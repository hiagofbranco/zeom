
const G="font-family:'Geist',Helvetica,Arial,sans-serif";
const T={canvas:'#F6F5EF',marfim:'#ECEADC',areia:'#DDD9C5',bege:'#BFBA99',oliva:'#6C664E',dourado:'#CCC290',ink:'#282621',brown:'#3A362C',border:'rgba(40,38,33,.14)'};
const sp=n=>`<div style="height:${n}px;line-height:${n}px;font-size:0">&nbsp;</div>`;
const hr=()=>`<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td style="border-top:1px solid ${T.border};font-size:0;line-height:0">&nbsp;</td></tr></table>`;
const eyebrow=(t,c=T.oliva)=>`<div style="${G};font-size:12px;font-weight:600;letter-spacing:0.8px;text-transform:uppercase;color:${c};mso-line-height-rule:exactly;line-height:16px">${t}</div>`;
const h1=(t,sz=24)=>`<div style="${G};font-size:${sz}px;font-weight:600;letter-spacing:-0.3px;color:${T.ink};mso-line-height-rule:exactly;line-height:${Math.round(sz*1.28)}px">${t}</div>`;
const p=(t,col=T.brown,sz=15,lh=23,w=300)=>`<p style="margin:0;${G};font-weight:${w};font-size:${sz}px;line-height:${lh}px;color:${col};mso-line-height-rule:exactly">${t}</p>`;

const solidBtn=(t,href)=>`<!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="${href}" style="height:48px;v-text-anchor:middle;width:280px;" arcsize="17%" strokecolor="${T.bege}" strokeweight="0" fillcolor="${T.bege}">
<w:anchorlock/>
<center style="color:${T.ink};font-family:Helvetica,Arial,sans-serif;font-size:14px;font-weight:600;">${t}</center>
</v:roundrect>
<![endif]-->
<!--[if !mso]><!-->
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="mso-hide:all"><tr><td align="center" bgcolor="${T.bege}" style="background-color:${T.bege};border-radius:8px">
<a href="${href}" target="_blank" style="display:inline-block;padding:14px 28px;${G};font-size:14px;font-weight:600;letter-spacing:0.1px;color:${T.ink};text-decoration:none;border-radius:8px;mso-hide:all">${t} &#8594;</a>
</td></tr></table>
<!--<![endif]-->`;

const outlineBtn=(t,href)=>`<!--[if mso]>
<v:roundrect xmlns:v="urn:schemas-microsoft-com:vml" xmlns:w="urn:schemas-microsoft-com:office:word" href="${href}" style="height:46px;v-text-anchor:middle;width:260px;" arcsize="17%" strokecolor="${T.border}" strokeweight="1px" fillcolor="${T.canvas}">
<w:anchorlock/>
<center style="color:${T.ink};font-family:Helvetica,Arial,sans-serif;font-size:13px;font-weight:600;">${t}</center>
</v:roundrect>
<![endif]-->
<!--[if !mso]><!-->
<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="mso-hide:all"><tr><td align="center" bgcolor="${T.canvas}" style="background-color:${T.canvas};border:1px solid ${T.border};border-radius:8px">
<a href="${href}" target="_blank" style="display:inline-block;padding:12px 24px;${G};font-size:13px;font-weight:600;color:${T.ink};text-decoration:none;border-radius:8px;mso-hide:all">${t} &#8594;</a>
</td></tr></table>
<!--<![endif]-->`;

const logoImg=(w=88)=>`<img src="{{ASSET_logo_wordmark}}" width="${w}" height="${Math.round(w*24/88)}" alt="zeom" style="display:block;width:${w}px;height:${Math.round(w*24/88)}px">`;

function header(kind,label){
 if(kind==='HA') return `<tr><td class="px" bgcolor="${T.canvas}" style="background-color:${T.canvas};padding:0 40px 28px;border-bottom:1px solid ${T.border}">${logoImg()}</td></tr>`;
 if(kind==='HB') return `<tr><td class="px" bgcolor="${T.canvas}" style="background-color:${T.canvas};padding:0 40px 28px;border-bottom:1px solid ${T.border}"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td align="left" valign="middle">${logoImg()}</td><td align="right" valign="middle"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td bgcolor="${T.marfim}" style="background-color:${T.marfim};border-radius:24px;padding:6px 14px;${G};font-size:11px;font-weight:600;letter-spacing:0.4px;text-transform:uppercase;color:${T.oliva}">${label}</td></tr></table></td></tr></table></td></tr>`;
 if(kind==='HC') return `<tr><td class="px" align="center" bgcolor="${T.canvas}" style="background-color:${T.canvas};padding:0 40px 28px;border-bottom:1px solid ${T.border};text-align:center"><table role="presentation" cellpadding="0" cellspacing="0" border="0" align="center"><tr><td>${logoImg()}</td></tr></table></td></tr>`;
 if(kind==='HD') return `<tr><td bgcolor="${T.dourado}" height="4" style="background-color:${T.dourado};height:4px;font-size:0;line-height:0">&nbsp;</td></tr><tr><td class="px" bgcolor="${T.canvas}" style="background-color:${T.canvas};padding:24px 40px 28px;border-bottom:1px solid ${T.border}">${logoImg()}</td></tr>`;
 if(kind==='HE') return `<tr><td class="px" bgcolor="${T.canvas}" style="background-color:${T.canvas};padding:0 40px 28px;border-bottom:1px solid ${T.border}"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td align="left" valign="middle">${logoImg()}</td><td align="right" valign="middle"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td bgcolor="${T.bege}" style="background-color:${T.bege};border-radius:24px;padding:6px 14px;${G};font-size:11px;font-weight:600;letter-spacing:0.2px;color:${T.ink}">${label}</td></tr></table></td></tr></table></td></tr>`;
}

function block(inner,pt=32,pb=32){return `<tr><td class="px" bgcolor="${T.canvas}" style="background-color:${T.canvas};padding:${pt}px 40px ${pb}px">${inner}</td></tr>`}

// trilha de progresso — círculos como <img> (Outlook não confia em border-radius)
function stepImg(state){ // done | active | pending
 return `<img src="{{ASSET_step_${state}}}" width="24" height="24" alt="" style="display:block;width:24px;height:24px">`;
}
function progressTrack(etapaLabel,steps,note){
 // steps: [{label,state}], state: done|active|pending
 const rows=steps.map((s,i)=>{
  const labelCol=s.state==='pending'? 'rgba(58,54,44,.45)':T.ink;
  const labelW=s.state==='active'?600:400;
  const connector = i<steps.length-1 ? `<tr><td width="24" align="center" style="width:24px;padding:2px 0"><table role="presentation" cellpadding="0" cellspacing="0" border="0"><tr><td width="2" height="20" bgcolor="${(s.state==='done')?T.oliva:T.areia}" style="width:2px;height:20px;background-color:${(s.state==='done')?T.oliva:T.areia};font-size:0;line-height:0">&nbsp;</td></tr></table></td><td></td><td></td></tr>`:'';
  return `<tr><td width="24" valign="top">${stepImg(s.state)}</td><td width="12" style="width:12px">&nbsp;</td><td valign="middle" style="padding:1px 0;${G};font-weight:${labelW};font-size:14px;line-height:24px;color:${labelCol}">${s.label}</td></tr>${connector}`;
 }).join('');
 return `<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="${T.marfim}" style="background-color:${T.marfim};border:1px solid ${T.border};border-radius:12px">
<tr><td style="padding:24px 24px 6px">${eyebrow('Progresso do cadastro',T.oliva)}${sp(6)}<div style="${G};font-weight:600;font-size:15px;letter-spacing:-0.1px;color:${T.ink};line-height:20px">${etapaLabel}</div></td></tr>
<tr><td style="padding:10px 24px 22px"><table role="presentation" cellpadding="0" cellspacing="0" border="0">${rows}</table></td></tr>
${note?`<tr><td style="padding:0 24px 22px;${G};font-weight:300;font-size:13px;color:${T.brown}">${note}</td></tr>`:''}
</table>`;
}

function codeBlock(label,value){
 return `<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="${T.marfim}" style="background-color:${T.marfim};border:1px solid ${T.border};border-radius:12px"><tr><td align="center" style="padding:28px 24px 26px">${eyebrow(label,T.oliva)}${sp(12)}<div class="code-val" style="${G};font-weight:600;font-size:36px;letter-spacing:8px;color:${T.ink};line-height:40px">${value}</div></td></tr></table>`;
}

function letterOpen(greeting,paragraphs,sign,role){
 return `${h1(greeting)}${sp(16)}${paragraphs.map(t=>p(t)+sp(14)).join('')}<div style="${G};font-weight:600;font-size:15px;color:${T.ink};line-height:20px">${sign}</div>${sp(2)}<div style="${G};font-style:italic;font-weight:300;font-size:13px;color:${T.oliva};line-height:18px">${role}</div>`;
}

function listIconLeft(items){
 return `<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">${items.map((it,i)=>`<tr><td width="40" valign="top" style="width:40px;padding:${i?'16px':'0'} 0 ${i<items.length-1?16:0}px"><img src="{{ASSET_ico_${it.icon}}}" width="28" height="28" alt="" style="display:block;width:28px;height:28px"></td><td valign="top" style="padding:${i?'16px':'0'} 0 ${i<items.length-1?16:0}px"><div style="${G};font-weight:600;font-size:14px;color:${T.ink};line-height:20px">${it.title}</div><div style="${G};font-weight:300;font-size:13px;color:${T.brown};line-height:19px;padding-top:3px">${it.desc}</div></td></tr>`).join('')}</table>`;
}
function listNumbered(items){
 return `<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">${items.map((it,i)=>`<tr><td width="32" valign="top" style="width:32px;padding:${i?'16px':'0'} 0 ${i<items.length-1?16:0}px"><div style="${G};font-weight:600;font-size:13px;color:${T.dourado};line-height:20px">0${i+1}</div></td><td valign="top" style="padding:${i?'16px':'0'} 0 ${i<items.length-1?16:0}px"><div style="${G};font-weight:600;font-size:14px;color:${T.ink};line-height:20px">${it.title}</div><div style="${G};font-weight:300;font-size:13px;color:${T.brown};line-height:19px;padding-top:3px">${it.desc}</div></td></tr>`).join('')}</table>`;
}
function listDivider(items){
 return `<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">${items.map((it,i)=>`<tr><td style="${i?'border-top:1px solid '+T.border+';':''}padding:${i?'14px':'0'} 0 14px"><div style="${G};font-weight:600;font-size:14px;color:${T.ink};line-height:20px">${it.title}</div><div style="${G};font-weight:300;font-size:13px;color:${T.brown};line-height:19px;padding-top:3px">${it.desc}</div></td></tr>`).join('')}</table>`;
}
function listStackedCards(items){
 return items.map((it,i)=>`${i?sp(10):''}<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="${T.marfim}" style="background-color:${T.marfim};border:1px solid ${T.border};border-radius:12px"><tr><td style="padding:16px 18px"><div style="${G};font-weight:600;font-size:14px;color:${T.ink};line-height:20px">${it.title}</div><div style="${G};font-weight:300;font-size:13px;color:${T.brown};line-height:19px;padding-top:3px">${it.desc}</div></td></tr></table>`).join('');
}
function listCompactCards(items){
 const cells=items.map((it,i)=>`<td width="${Math.floor(100/items.length)}%" valign="top" style="width:${Math.floor(100/items.length)}%;${i?'padding-left:8px':''}"><table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="${T.marfim}" style="background-color:${T.marfim};border:1px solid ${T.border};border-radius:12px"><tr><td style="padding:16px 14px"><div style="${G};font-weight:600;font-size:13px;color:${T.ink};line-height:18px">${it.title}</div><div style="${G};font-weight:300;font-size:12px;color:${T.brown};line-height:17px;padding-top:5px">${it.desc}</div></td></tr></table></td>`).join('');
 return `<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr>${cells}</tr></table>`;
}

function openQuestion(question,cta,href){
 return `<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="${T.marfim}" style="background-color:${T.marfim};border:1px solid ${T.border};border-radius:12px"><tr><td style="padding:22px 22px 24px">${p(question,T.ink,15,23,400)}${sp(18)}${outlineBtn(cta,href)}</td></tr></table>`;
}

function complementary(eyebrowTxt,titleTxt,bodyTxt,cta,href,variant){
 // variant: 'line' plain text link row, 'chip' icon pill row — visual variety for repeated topics
 if(variant==='chip'){
  return `${eyebrow(eyebrowTxt,T.oliva)}${sp(10)}<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="${T.marfim}" style="background-color:${T.marfim};border:1px solid ${T.border};border-radius:12px"><tr><td style="padding:18px 20px"><div style="${G};font-weight:600;font-size:14px;color:${T.ink};line-height:20px">${titleTxt}</div>${sp(6)}${p(bodyTxt,T.brown,13,19)}${sp(14)}${outlineBtn(cta,href)}</td></tr></table>`;
 }
 return `${eyebrow(eyebrowTxt,T.oliva)}${sp(10)}${h1(titleTxt,17)}${sp(8)}${p(bodyTxt,T.brown,13,19)}${sp(16)}${outlineBtn(cta,href)}`;
}

function instaMockup(){
 return `<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td align="center" style="padding:4px 0 20px"><img src="{{ASSET_mockup_instagram_zeom}}" width="220" alt="" style="display:block;width:220px;max-width:100%;height:auto"></td></tr></table>`;
}

function footer(text){
 return `<tr><td class="px" bgcolor="${T.canvas}" style="background-color:${T.canvas};padding:40px 40px 32px">${hr()}<div style="padding-top:20px;${G};font-weight:300;font-size:11px;line-height:17px;color:${T.oliva}">${text}<br>{{RAZAO_SOCIAL}} · {{ENDERECO_POSTAL}}</div></td></tr>`;
}

function shell(title,preheader,body){
 return `<!DOCTYPE html>
<html lang="pt-BR" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light">
<meta name="supported-color-schemes" content="light">
<title>${title}</title>
<!--[if mso]>
<noscript><xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml></noscript>
<![endif]-->
<style>
body,table,td{margin:0;padding:0}
img{border:0;outline:none;text-decoration:none;-ms-interpolation-mode:bicubic}
table{border-collapse:collapse}
@media (max-width:480px){
  .container{width:100% !important;max-width:100% !important}
  .px{padding-left:24px !important;padding-right:24px !important}
  .code-val{font-size:30px !important;letter-spacing:5px !important}
}
</style>
</head>
<body style="margin:0;padding:0;background-color:${T.canvas};-webkit-font-smoothing:antialiased">
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;font-size:1px;line-height:1px;color:${T.canvas};opacity:0">${preheader}&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;&nbsp;&#8203;</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" bgcolor="${T.canvas}" style="background-color:${T.canvas}">
<tr><td align="center" style="padding:32px 12px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" class="container" style="width:600px;max-width:600px">
${body}
</table>
</td></tr>
</table>
</body>
</html>`;
}

Object.assign(globalThis,{T,sp,hr,eyebrow,h1,p,solidBtn,outlineBtn,logoImg,header,block,stepImg,progressTrack,codeBlock,letterOpen,listIconLeft,listNumbered,listDivider,listStackedCards,listCompactCards,openQuestion,complementary,instaMockup,footer,shell});
