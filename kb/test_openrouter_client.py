"""Offline boundary tests; no real API calls and no credentials required."""
import copy
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch
import openrouter_client as api
import retrieve

KEY="sk-or-"+"test-not-a-real-key-000000000000"
class Response(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self,*args): self.close()
class Transport:
    def __init__(self,content="CarDoctor API ready",finish="stop"):
        self.calls=[]
        self.body=json.dumps({"choices":[{"finish_reason":finish,"message":{"content":content}}],"usage":{"prompt_tokens":8,"completion_tokens":4,"cost":0.000002,"extra":"not retained"}}).encode()
    def open(self,request,timeout):
        self.calls.append((request,timeout))
        return Response(self.body)

class OpenRouterTests(unittest.TestCase):
    def setUp(self):
        self.config=api.Config(KEY)
        self.bundle=retrieve.retrieve("outward bulge on tyre sidewall",part="tire",limit=1)
        r=self.bundle["evidence"][0]
        self.answer={"claims":[{
            "kind":"next_step","text":r["actions"][0],"record_id":r["id"],"source_id":r["source_refs"][0]["source_id"]}],
            "follow_up_questions":[],"repair_cost":None,"diagnosis":None}
    def test_env_quotes_and_override(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/".env"
            p.write_text('OPENROUTER_API_KEY="'+KEY+'"'+chr(10)+'OPENROUTER_MAX_TOKENS=800',encoding="utf-8")
            config=api.read_config(p,{"OPENROUTER_MAX_TOKENS":"700"})
            self.assertEqual(config.key,KEY)
            self.assertEqual(config.max_tokens,700)
            self.assertNotIn(KEY,repr(config))
    def test_placeholder_never_calls(self):
        transport=Transport()
        with self.assertRaises(api.APIError): api.send(api.Config("sk-or-xxx"),[],opener=transport)
        self.assertEqual(transport.calls,[])
    def test_invalid_bounds_and_model(self):
        for config in [api.Config(KEY,max_tokens=5000),api.Config(KEY,timeout=1),api.Config(KEY,model="other")]:
            with self.assertRaises(api.APIError): config.validate()
    def test_env_invalid_number_is_redacted(self):
        with self.assertRaises(api.APIError) as e: api.read_config("does-not-exist",{"OPENROUTER_MAX_TOKENS":KEY})
        self.assertNotIn(KEY,str(e.exception))
    def test_request_matches_endpoint_and_budget(self):
        transport=Transport()
        text,metadata=api.send(self.config,[{"role":"user","content":"hello"}],max_tokens=32,opener=transport)
        req,timeout=transport.calls[0]
        self.assertEqual(req.full_url,api.ENDPOINT)
        self.assertEqual(req.get_header("Authorization"),"Bearer "+KEY)
        payload=json.loads(req.data)
        self.assertEqual(payload["max_tokens"],32)
        self.assertFalse(payload["stream"])
        self.assertEqual(payload["provider"],{"require_parameters":True})
        self.assertNotIn("extra",metadata["usage"])
    def test_no_redirect(self):
        self.assertIsNone(api.NoRedirect().redirect_request(None,None,302,"",{},"https://elsewhere.invalid"))
    def test_truncation_rejected_no_retry(self):
        transport=Transport(finish="length")
        with self.assertRaises(api.APIError): api.send(self.config,[],opener=transport)
        self.assertEqual(len(transport.calls),1)
    def test_http_error_never_echoes_remote_body(self):
        transport=Transport()
        transport.open=lambda *a,**kw: (_ for _ in ()).throw(urllib.error.HTTPError(api.ENDPOINT,401,KEY,{},io.BytesIO(KEY.encode())))
        with self.assertRaises(api.APIError) as e: api.send(self.config,[],opener=transport)
        self.assertNotIn(KEY,str(e.exception))
        self.assertIn("401",str(e.exception))
    def test_oversize_before_network(self):
        transport=Transport()
        with self.assertRaises(api.APIError): api.send(self.config,[{"content":"x"*50000}],opener=transport)
        self.assertEqual(transport.calls,[])
    def test_generated_output_preserves_source_conditions(self):
        transport=Transport(json.dumps(self.answer))
        result=api.explain(self.bundle,self.config,opener=transport)
        self.assertEqual(result["status"],"generated_unreviewed")
        self.assertEqual(result["conditions_and_limits"][0]["urgency"],self.bundle["evidence"][0]["urgency"])
        payload=json.loads(transport.calls[0][0].data)
        self.assertEqual(payload["response_format"]["type"],"json_schema")
        self.assertNotIn(KEY,json.dumps(result))
    def test_observations_are_application_owned(self):
        result=api.explain(self.bundle,self.config,opener=Transport(json.dumps(self.answer)))
        self.assertEqual(result["reported_observations"]["user_report"],self.bundle["query"])
        self.assertFalse(result["reported_observations"]["verified"])
        bad={**self.answer,"observations":"An uncited interpretation"}
        with self.assertRaises(api.APIError): api.validate_answer(bad,self.bundle)

    def test_unretrieved_and_unbound_citations_rejected(self):
        for field,value in [("record_id","K999"),("source_id","S999"),("source_id","S02")]:
            bad=copy.deepcopy(self.answer);bad["claims"][0][field]=value
            with self.assertRaises(api.APIError): api.validate_answer(bad,self.bundle)
    def test_cost_diagnosis_extra_fields_rejected(self):
        for field,value in [("repair_cost",100),("diagnosis","failed tyre"),("extra","oops")]:
            bad=copy.deepcopy(self.answer);bad[field]=value
            with self.assertRaises(api.APIError): api.validate_answer(bad,self.bundle)
    def test_non_json_and_wrong_citation_fallback(self):
        for content in ["not JSON",json.dumps({**self.answer,"repair_cost":20})]:
            result=api.explain(self.bundle,self.config,opener=Transport(content))
            self.assertEqual(result["status"],"deterministic_fallback")
            self.assertIsNone(result["generated_answer"])
    def test_missing_context_and_unknown_never_call(self):
        for bundle in [retrieve.retrieve("quantum banana",part="body"),retrieve.retrieve("oil light",part="dashboard")]:
            transport=Transport()
            result=api.explain(bundle,self.config,opener=transport)
            self.assertFalse(result["api_called"])
            self.assertEqual(transport.calls,[])

if __name__=="__main__": unittest.main()
