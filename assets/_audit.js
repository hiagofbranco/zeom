const IMGBG={'grad-escuro.jpg':'#262620','grad-escuro-ouro.jpg':'#2C2C25','grad-areia.jpg':'#2A2A24','grad-marfim-areia.jpg':'#303029','grad-ouro.jpg':'#B5AC80','grad-ouro-horiz.jpg':'#B5AC80','prot-janela-aviao.jpg':'#21211C','prot-mar.jpg':'#21211C','prot-louvre.jpg':'#21211C','prot-eiffel.jpg':'#21211C','prot-skyline-janela.jpg':'#21211C','prot-nuvens.jpg':'#21211C'};
const lum=h=>{const v=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(c=>c<=0.03928?c/12.92:Math.pow((c+0.055)/1.055,2.4));return .2126*v[0]+.7152*v[1]+.0722*v[2]};
const ratio=(a,b)=>{const l1=lum(a),l2=lum(b);return +(((Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05))).toFixed(2)};
function run(html){const doc=new DOMParser().parseFromString(html,'text/html');
 const bgOf=el=>{let n=el;while(n&&n!==doc.body){const st=(n.getAttribute&&n.getAttribute('style'))||'';
  const bgi=(n.getAttribute&&n.getAttribute('background'))||'';const m2=bgi.match(/([a-z0-9-]+\.jpg)/);
  if(m2&&IMGBG[m2[1]])return IMGBG[m2[1]];
  const m=st.match(/background(?:-color)?:\s*(#[0-9A-Fa-f]{6})/);if(m)return m[1].toUpperCase();
  const bc=n.getAttribute&&n.getAttribute('bgcolor');if(bc&&/^#[0-9A-Fa-f]{6}$/.test(bc))return bc.toUpperCase();
  n=n.parentElement}return '#21211C'};
 const out=[];
 doc.querySelectorAll('[style*="color:"]').forEach(el=>{const st=el.getAttribute('style')||'';
  const m=st.match(/(?:^|;)\s*color:\s*(#[0-9A-Fa-f]{6})/);if(!m)return;
  const fg=m[1].toUpperCase();const txt=(el.textContent||'').replace(/\s+/g,' ').trim();if(!txt)return;
  const bg=bgOf(el.parentElement||el);const r=ratio(fg,bg);
  if(r<4.5)out.push({fg,bg,r,txt:txt.slice(0,40)})});
 return out}