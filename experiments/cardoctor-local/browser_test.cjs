// Local UI engineering fixtures only. Uses preinstalled Chrome and a D: profile.
const fs=require('fs'),path=require('path'),cp=require('child_process');
const {chromium}=require('playwright');
const base=__dirname,runtime=path.join(base,'.runtime','ui-tests',Date.now().toString());
fs.mkdirSync(path.join(runtime,'cache','torch','checkpoints'),{recursive:true});
fs.mkdirSync(path.join(runtime,'tmp'),{recursive:true});
const weight=path.join(runtime,'cache','torch','checkpoints','resnet18-f37072fd.pth');
if(!fs.existsSync(weight))fs.linkSync(path.join(base,'.runtime','cache','torch','checkpoints','resnet18-f37072fd.pth'),weight);
const env={...process.env,CARDOCTOR_RUNTIME:runtime,PYTHONDONTWRITEBYTECODE:'1',TEMP:path.join(runtime,'tmp'),TMP:path.join(runtime,'tmp')};
const server=cp.spawn('D:\\hakathon_wiut\\.venv\\Scripts\\python.exe',['-u','server.py'],{cwd:base,env,windowsHide:true,stdio:['ignore','pipe','pipe']});
let logs='';server.stdout.on('data',b=>logs+=b);server.stderr.on('data',b=>logs+=b);
const assert=(condition,message)=>{if(!condition)throw Error(message)};
(async()=>{
 let context;
 const started=Date.now(),errors=[],checks=[];
 try{
  let ready=false;for(let i=0;i<60;i++){try{const r=await fetch('http://127.0.0.1:8765/api/health');const h=await r.json();if(h.storage===runtime){ready=true;break}}catch{}await new Promise(r=>setTimeout(r,500))}assert(ready,'QA server did not start');
  context=await chromium.launchPersistentContext(path.join(runtime,'browser-profile'),{executablePath:'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',headless:true,viewport:{width:1280,height:1000},env,args:['--disk-cache-dir='+path.join(runtime,'browser-cache'),'--disable-background-networking','--disable-component-update','--no-first-run']});
  const page=context.pages()[0];page.on('pageerror',error=>errors.push(error.message));page.on('console',msg=>{if(msg.type()==='error')errors.push(msg.text())});
  await page.goto('http://127.0.0.1:8765');await page.getByText('Vision model ready',{exact:true}).waitFor();assert(await page.locator('#refCount').innerText()==='0','Fresh QA library not empty');checks.push('Fresh empty state and model health render');
  await page.screenshot({path:path.join(runtime,'01-empty-desktop.png'),fullPage:true});
  await page.getByRole('button',{name:/Source notes/}).click();await page.getByLabel('Title',{exact:true}).fill('Synthetic crack source - engineering test');await page.getByLabel('Reviewed excerpt or source summary').fill('Crack source fixture only; not vehicle advice.');await page.getByLabel('Source URL').fill('https://example.org/engineering-fixture');await page.getByLabel('Search terms').fill('crack');await page.getByLabel('I checked the passage and its vehicle applicability.').check();await page.getByRole('button',{name:'Add reviewed note'}).click();await page.getByText('Reviewed source note saved on D:.').waitFor();assert(await page.locator('#noteCount').innerText()==='1','Note count failed');checks.push('Add reviewed source through form');
  await page.getByRole('button',{name:/Inspect a photo/}).click();
  const create=cp.spawnSync('D:\\hakathon_wiut\\.venv\\Scripts\\python.exe',['-c','from PIL import Image,ImageDraw; from pathlib import Path; p=Path(r"'+runtime+'"); im=Image.new("RGB",(640,480),(228,231,235)); d=ImageDraw.Draw(im); d.rectangle((100,100,480,360),fill=(50,120,180)); im.save(p/"synthetic-rectangle.png"); d.line((120,130,420,320),fill=(240,40,30),width=8); im.save(p/"synthetic-query.png")'],{env,windowsHide:true});assert(create.status===0,'Fixture creation failed');
  await page.locator('#imageFile').setInputFiles(path.join(runtime,'synthetic-rectangle.png'));await page.locator('#imageCanvas').waitFor({state:'visible'});await page.getByRole('button',{name:'Find similar evidence'}).waitFor({state:'visible'});
  const rect=await page.locator('#imageCanvas').boundingBox();await page.mouse.move(rect.x+rect.width*.15,rect.y+rect.height*.15);await page.mouse.down();await page.mouse.move(rect.x+rect.width*.85,rect.y+rect.height*.85,{steps:8});await page.mouse.up();assert((await page.locator('#regionInfo').innerText()).includes('Selected region'),'Region drag failed');checks.push('Photo upload and manual region drag');
  await page.getByRole('button',{name:'Add this photo as a reference'}).click();await page.getByLabel('Reviewed visible label').fill('synthetic rectangle');await page.getByLabel('Vehicle / incident group',{exact:true}).fill('synthetic-group-A');await page.getByLabel('Source',{exact:true}).fill('Generated UI test fixture - not damage');await page.getByLabel('Permission / reuse basis').fill('Original synthetic engineering fixture');await page.getByRole('button',{name:'Add reference',exact:true}).click();await page.getByText(/Reference saved on D:/).waitFor();checks.push('Reference dialog saves metadata and selected region');
  await page.locator('#imageFile').setInputFiles(path.join(runtime,'synthetic-query.png'));await page.getByLabel('Your description').fill('crack test');await page.getByRole('button',{name:'Find similar evidence'}).click();await page.locator('#results').waitFor({state:'visible'});await page.locator('#matches').getByText('synthetic rectangle',{exact:true}).waitFor();await page.locator('#evidence').getByText('Synthetic crack source - engineering test',{exact:true}).waitFor();checks.push('Neural reference retrieval and sourced-text retrieval render');
  await page.getByRole('button',{name:'Save Markdown on D:'}).click();await page.getByText(/Markdown report saved on D:/).waitFor();assert(fs.readdirSync(path.join(runtime,'reports')).some(n=>n.endsWith('.md')),'Report export missing');checks.push('Markdown report written by server to D:');
  await page.screenshot({path:path.join(runtime,'02-evidence-desktop.png'),fullPage:true});
  await page.setViewportSize({width:390,height:844});await page.screenshot({path:path.join(runtime,'03-evidence-mobile.png'),fullPage:true});const overflow=await page.evaluate(()=>document.documentElement.scrollWidth>window.innerWidth);assert(!overflow,'Mobile page overflows horizontally');checks.push('390px mobile layout has no horizontal overflow');
  assert(errors.length===0,'Browser errors: '+errors.join('; '));checks.push('No browser JavaScript or console errors');
  const result={status:'passed',checks,seconds:(Date.now()-started)/1000,fixture_notice:'All QA photos and source notes are synthetic engineering fixtures, not damage data.',runtime};fs.writeFileSync(path.join(runtime,'UI-RESULTS.json'),JSON.stringify(result,null,2));console.log(JSON.stringify(result,null,2));
 }finally{if(context)await context.close();server.kill();fs.writeFileSync(path.join(runtime,'server-test.log'),logs)}
})().catch(error=>{console.error(error.stack);process.exitCode=1});


