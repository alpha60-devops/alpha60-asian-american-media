import assert from 'node:assert/strict';
import {mkdir,writeFile} from 'node:fs/promises';
const [base,out,endpoint='http://127.0.0.1:9236']=process.argv.slice(2);
await mkdir(out,{recursive:true});
const target=await (await fetch(endpoint+'/json/new?about:blank',{method:'PUT'})).json();
const ws=new WebSocket(target.webSocketDebuggerUrl);
await new Promise(r=>ws.addEventListener('open',r,{once:true}));
let id=0;const pending=new Map();
ws.addEventListener('message',({data})=>{const m=JSON.parse(data);if(m.id){const p=pending.get(m.id);pending.delete(m.id);m.error?p.reject(m.error):p.resolve(m.result);}});
const send=(method,params={})=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});ws.send(JSON.stringify({id:n,method,params}));});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,returnByValue:true,awaitPromise:true});if(r.exceptionDetails)throw Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
const receipt={pages:[]};
try {
 await send('Page.enable');await send('Runtime.enable');await send('Page.bringToFront');await send('Emulation.setFocusEmulationEnabled',{enabled:true});
 for(const width of [1440,390]) {
  await send('Emulation.setDeviceMetricsOverride',{width,height:1000,deviceScaleFactor:1,mobile:false});
  await send('Page.navigate',{url:base+'docs/godzilla.html'});
  for(let i=0;i<600;i++) {
   if(await evaluate("document.readyState==='complete'&&document.querySelectorAll('.gojira-h3[data-ready=true]').length===4"))break;
   await new Promise(r=>setTimeout(r,100));
  }
  const stats=await evaluate(`({width:innerWidth,scroll:document.documentElement.scrollWidth,portraits:document.querySelectorAll('.gojira-portraits img').length,maps:document.querySelectorAll('.gojira-h3[data-ready=true]').length,graphs:document.querySelectorAll('svg[id^="mellon-7.8-stage5-"][id$=-weekly]').length,broken:[...document.images].filter(x=>!x.complete||!x.naturalWidth).map(x=>x.src)})`);
  assert.equal(stats.portraits,4);assert.equal(stats.maps,4);assert.equal(stats.broken.length,0);assert(stats.scroll<=width+1,JSON.stringify(stats));assert.equal(stats.graphs,8);
  assert(await evaluate("document.querySelector('main').textContent.includes('weeks 1–26')"));
  const layout=await evaluate("[...document.querySelector('.gojira-portraits').children].map(e=>({x:e.getBoundingClientRect().x,y:e.getBoundingClientRect().y}))");
  assert(width>700 ? layout[0].y===layout[1].y : layout[0].y<layout[1].y);
  for(let index=0;index<4;index++) {
   const selector=`document.querySelectorAll('.gojira-h3')[${index}]`;
   const controls=await evaluate(`(()=>{const root=${selector},before=root.querySelector('[data-status]').textContent;for(const [sel,value] of [['[data-role]','uploaders'],['[data-mode]','without-hosting']]){const e=root.querySelector(sel);e.value=value;e.dispatchEvent(new Event('change'));}const c=root.querySelector('[data-coverage]');c.checked=true;c.dispatchEvent(new Event('change'));const missing=[...root.querySelectorAll('.h3-point')].filter(e=>e.getAttribute('fill')==='none'&&e.style.display!=='none');const visible=[...root.querySelectorAll('.h3-point')].filter(e=>e.style.display!=='none');const point=visible.find(e=>e.getAttribute('fill')!=='none');point.focus();return {before,missing:missing.length,radii:[...new Set(visible.map(e=>e.getAttribute('r')))],detail:root.querySelector('[data-detail]').textContent,rows:root.querySelectorAll('tbody tr').length,cells:root.querySelectorAll('.h3-point').length};})()`);
   assert(controls.missing>0);assert.deepEqual(controls.radii,['6']);assert.equal(controls.rows,controls.cells);assert(controls.detail.includes('uploaders, without-hosting'));assert(!controls.detail.includes('-0.000 pp'));
  }
  const city=await evaluate(`(()=>{const root=document.getElementById('mellon-7.8-stage5-city-films'),c=root.querySelector('circle[data-tooltip]');c.focus();return {label:c.getAttribute('aria-label'),tip:root.closest('figure').querySelector('.map-tooltip').textContent,radii:[...new Set([...root.querySelectorAll('circle[data-tooltip]')].map(e=>e.getAttribute('r')))]};})()`);
  assert(city.label.includes('Hot:')||city.label.includes('Cold:'));assert(city.tip.includes('Weeks 1–26'));assert.deepEqual(city.radii,['6']);
  assert(await evaluate("document.querySelectorAll('[data-hover-ready=true]').length>=56"));
  const ids=await evaluate("[...document.querySelectorAll('svg[id^=\"mellon-7.8-stage5-\"][id$=-weekly]')].map(e=>e.id)");
  for(const graph of ids) {
   await evaluate(`{const e=document.getElementById(${JSON.stringify(graph)});if(e.closest('details'))e.closest('details').open=true;e.querySelector('.izzi-line-series').focus();}`);
   await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Enter',code:'Enter',windowsVirtualKeyCode:13,text:'\r'});
   assert(await evaluate(`[...document.getElementById(${JSON.stringify(graph)}).querySelector('.izzi-line-series').querySelectorAll('polyline')].some(e=>e.style.stroke==='red')`));
   await send('Input.dispatchKeyEvent',{type:'keyUp',key:'Enter',code:'Enter',windowsVirtualKeyCode:13});
   await send('Input.dispatchKeyEvent',{type:'keyDown',key:'Escape',code:'Escape',windowsVirtualKeyCode:27});
  }
  const links=await evaluate(`(async()=>{const urls=[...new Set([...document.querySelectorAll('main a[href]')].map(a=>a.href).filter(h=>new URL(h).origin===location.origin))];const results=[];for(const url of urls){const r=await fetch(url);results.push({url,status:r.status});}return results;})()`);
  assert(links.every(r=>r.status===200),JSON.stringify(links.filter(r=>r.status!==200)));stats.localLinks=links.length;
  const large=await evaluate(`Promise.all([...document.querySelectorAll('.gojira-portraits figure>a')].map(a=>new Promise(resolve=>{const i=new Image;i.onload=()=>resolve(Math.max(i.naturalWidth,i.naturalHeight));i.onerror=()=>resolve(0);i.src=a.href;})))`);assert.deepEqual(large,[3840,3840,3840,3840]);
  for(const [name,selector] of [['japan','.gojira-portraits'],['h3','.gojira-h3'],['weekly','#mellon-7\\.8-stage5-films-downloaders-all-weekly']]) {
   await evaluate(`document.querySelector(${JSON.stringify(selector)}).scrollIntoView()`);
   const shot=await send('Page.captureScreenshot',{format:'png'});await writeFile(`${out}/${name}-${width}.png`,Buffer.from(shot.data,'base64'));
  }
  receipt.pages.push({...stats,status:'PASS',controls:['role','hosting','unavailable cells','keyboard focus','weekly series keyboard interaction'],highResolution:large});
 }
 receipt.status='PASS';await writeFile(out+'/browser.json',JSON.stringify(receipt,null,2)+'\n');console.log(JSON.stringify(receipt));
}finally{ws.close();await fetch(endpoint+'/json/close/'+target.id);}
