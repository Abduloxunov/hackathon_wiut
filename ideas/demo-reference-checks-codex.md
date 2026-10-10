# Supplied projects and demo links — verification notes

Checked by Bexruz + codex on 10 Oct 2026 for the [six refined proposals](refined-six-ideas-codex.md). This is a reference catalogue, not our implementation, dataset or performance evidence.

**Scope of checking:** YouTube's public oEmbed metadata confirmed the titles and publishers of ten supplied videos. It did not confirm full playback or independently validate their contents, accuracy, deployment, licences or business results. No videos were downloaded. The ACTi link returned HTTP 401 to the metadata check; its title/publisher remain unverified, which does not prove it is permanently unavailable. Web sources below were read where accessible; access limits are explicit.

## Vehicle inspection videos supplied by Bexruz

| Link and confirmed title | Confirmed publisher | How to use the reference / what remains unverified |
|---|---|---|
| [AI Vehicle Damage Detection on AWS — Automated Repair Estimates](https://www.youtube.com/watch?v=r79zcpxTtKk) | NeenOpal | Product/demo reference for damage and estimates. The supplied Pavel Motors relationship and any real-price accuracy are not verified by metadata. |
| [Car Damage Detection Demo](https://www.youtube.com/watch?v=kZgzOiw9ZXo) | Intelliarts | Damage-demo reference. Two-model architecture and availability/licence of the mentioned Hugging Face Space were not verified in this check. |
| [AI for vehicle inspection, damages & claims management — Demonstration](https://www.youtube.com/watch?v=gtBRn6FDICc) | WeProov | Inspection/claims workflow reference. A demonstration is not independent accuracy or deployment evidence. |
| [AI Car Inspection Demonstration BONUS FOOTAGE](https://www.youtube.com/watch?v=QlP1NTvmGgo) | NBC New York | News demonstration. Metadata does not establish the supplier association; use the Hertz primary source below for the separate UVeye implementation example. |
| [Carscan App demo](https://www.youtube.com/watch?v=A4vGvXP8ViY) | Carscan AI | App-demo reference; test workflow ideas, not vendor metrics as our results. |
| [Carscan explainer video](https://www.youtube.com/watch?v=OTLRPzb1OaQ) | Carscan AI | Explainer; distinguish it from the app-demo link above. |
| [Car Damage Detection Project Using Python, YOLOv8, and OpenCV](https://www.youtube.com/watch?v=lqPGBEZPRr0) | PySeek | Tutorial/project reference. Do not present it as a confirmed commercial rollout or assume source/checkpoint permission. |
| [A System for Automated Vehicle Damage Localization and Severity Estimation Using Deep Learning](https://www.youtube.com/watch?v=LwrPTsrhW9Y) | JP INFOTECH PROJECTS | Project presentation. Title alone does not establish research validation, physical severity accuracy or customer deployment. |

[DAMAGE iD's primary demo page](https://www.damageid.com/blog/damage-id-new-automatic-damage-detection-demo/) is accessible and links its video. The vendor describes a 2021 controlled demonstration using a model car and chalk marks, followed by guided photos and a cloud review portal. That is useful inspiration for an honest live test; it is not proof that a marked toy behaves like real scratched paint.

[Hertz's announcement, 16 April 2025](https://newsroom.hertz.com/articles/article-details/hertz-and-uveye-partner-to-modernize-vehicle-maintenance-with-ai-technology/) states that UVeye installations began at Atlanta airport and a broader rollout was planned. This is customer-side implementation evidence for dedicated camera inspection. It does not verify that every planned rollout finished, or transfer scanner performance to ordinary phone photos. Treat accuracy/speed language in announcements as supplier/customer claims, not our benchmarks.

## Road, driver and plate references supplied by Bexruz

| Reference | Check and relevance |
|---|---|
| [Road Damage Detection Demo — Putrajaya, Malaysia](https://www.youtube.com/watch?v=g_Djlz7WHHc) | Metadata title includes `2026-03-29, 9:34am`; publisher is aireka-innovission-aisense. Road-demo reference. Edge/GPS/cloud architecture and sustained deployment were not verified by metadata. |
| [Bentley Blyncsy product page](https://www.bentley.com/en/products/blyncsy/) | Official page contains a product-video option. For implementation evidence, [Hawaiʻi DOT's January 2026 programme announcement](https://hidot.hawaii.gov/highways/next-steps-for-eyes-on-the-road/) describes dash-camera collection with UH and Blyncsy for maintenance staff. Neither source establishes our local accuracy. |
| [IEEE Spectrum's Nauto article](https://spectrum.ieee.org/ai-dashcam-driver-safety-nauto) | Supplied secondary reference. Technical evidence should come from primary material. [Nauto's VTTI study page](https://www.nauto.com/vtti/study-report) and [risk-fusion study page](https://www.nauto.com/vtti/risk-fusion-report) summarise commissioned testing and offer gated reports. Full reports were not obtained; do not quote their headline numbers as independent universal benchmarks. Nauto states VTTI does not endorse products. |
| Samsara AI dash cameras | Supplied suggestion did not contain a specific video URL. Attempts to retrieve candidate official safety pages failed in this check. No new demo URL or numerical claim is treated as verified. |
| [Motive AI dash-camera product page](https://gomotive.com/products/ai-dashcam/) | Official product page accessible; product reference for event detection/coaching. No specific supplied demo video or independently checked accuracy result. |
| [License plate detection and recognition demo using NVIDIA pre-trained models](https://www.youtube.com/watch?v=p91epBEfISk) | Confirmed publisher: NVIDIA Developer. Model demo, not evidence of Uzbek-plate performance, customer-record integration or permission for personal data. |
| [Placa.ai LPR camera demos](https://www.placa.ai/lpr-camera-demo/) | Official demo-listing page accessible. Do not use marketing accuracy or deployment assertions without separate evidence. |
| [Supplied ACTi dealer/service-centre video](https://www.youtube.com/watch?v=JNghUo5a7cY) | Metadata retrieval returned HTTP 401. Attribution, title and content unverified; not relied on for the proposals. |

Plate recognition is optional background research, not a required feature of these six refined MVPs. Synthetic identifiers and case IDs avoid introducing unnecessary customer/plate dependencies.

## Additional primary sources for scope and data

- [Partium image-search documentation](https://docs.partium.io/partium-find/partium-search-engine/how-partium-image-part-search-works/): describes image/text queries combined with catalogue master data. Relevant prior art for parts; it does not grant catalogue, patent, code or model rights.
- [WACV 2020 helmet-detection paper](https://openaccess.thecvf.com/content_WACV_2020/html/Chairat_Low_Cost_High_Performance_Automatic_Motorcycle_Helmet_Violation_Detection_WACV_2020_paper.html): primary research on detection/classification/tracking. Not a blanket licence for source videos or weights; its performance is not ours.
- [Open Charge Alliance OCPP overview](https://openchargealliance.org/protocols/open-charge-point-protocol/): charger-to-management-system communication. Protocol existence is not access to a partner's charger feed.
- [Humans in the Loop exterior parts/damage dataset](https://humansintheloop.org/resources/datasets/car-parts-and-car-damages-dataset/): publisher's indexed content lists CC0 1.0 and an access form. Direct page retrieval failed during this batch, but the primary search result returned its licence text. It is a candidate, not data we have downloaded or privacy-cleared.
- [RDD2022 original record](https://figshare.com/articles/dataset/RDD2022_-_The_multi-national_Road_Damage_Dataset_released_through_CRDDC_2022/21431547): HTML retrieval failed; the [original publisher API](https://api.figshare.com/v2/articles/21431547) was fetched directly and returned CC BY 4.0 and DOI `10.6084/m9.figshare.21431547.v1`. Keep the exact release's attribution. This does not establish permissions for unrelated pretrained weights or identifiable people/plates.
- [RoadDamageDetector repository](https://github.com/sekilab/RoadDamageDetector): repository lists MIT code. Check dataset and checkpoint terms separately; do not propagate a mirror's conflicting licence label as the original dataset licence.

## How the team should cite these

Label demos as competitor examples, research as prior art and synthetic experiments as controlled tests. Do not copy footage or code without rights, present earlier/outsider work as finals work, infer customer adoption from a YouTube title, or borrow someone else's numbers for our deck. Before using a model, save the actual licence and artifact version; before showing footage, check the challenge's consent rules as well as copyright terms.
