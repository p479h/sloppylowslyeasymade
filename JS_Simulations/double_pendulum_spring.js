//First the params of the pendulums
let θa, dθa, θb, dθb, ma, mb, xa, ya, xb, yb, la, lb, va, vb;
let separation; //Distance between pivots

//Ohter params
let nskip, t, dt, g, updated;

//Then the params of the spring
let li, L, k;

//Drawing elements
let W, H, bg, font, canvas;

//Widgets
let entries = {
  dt: null,
  nskip: null
};

let sliders = {
  li: null,
  la: null,
  lb: null,
  ma: null,
  mb: null,
  θa: null,
  θb: null,
};

function setDefaults(){
  //First canvas elements
  W = 650, H = 400;

  //Parameters of pendulums
  θa = θb = 3.141;
  ma = mb = 1;
  la = lb = 300;
  separation = 150;
  xa = sin(θa)*la; ya = yb = cos(θa)*la;
  xb = xa+separation;
  va = vb = 0;

  //Parameters of the spring
  li = separation;
  L = sqrt((xa-xb)**2+(ya-yb)**2);
  k=0.1;

  //Other parameters
  nskip = 50;
  dt = 0.001;
  t = 0;
  g = 9.8;
  updated = false;
};

function makeAxis(x, y, w, h, xlabel, ylabel){
  strokeWeight(3);
  textSize(12);
  line(x, y, x+w, y);
  line(x, y, x, y-h);
  triangle(x+w, y+h/20, x+w, y-h/20, x+w+h/15, y);
  triangle(x-h/20, y-h, x+h/20, y-h, x, y-h-h/15);
  strokeWeight(0);
  text(xlabel, x+0.9*w, y+h/4);
  text(ylabel, x-w/6, y-h*0.9);
};

function dashLine(x0, y0, n, s1, s2, dir){
  let x1 = x0, y1 = y0;
  if (dir == 'x') {x1+=s1} else {y1+=s1};
  while (n--) {
    line(x0, y0, x1, y1);
    if (dir == 'x') {x1+=s2; x0+=s2} else {y1+=s2; y0+=s2};
  };
};

function resetBg(){
  background(20);
  fill(50);
  stroke(70);
  strokeWeight(2);
  rect(0, 0, W, H/4);
  rect(0, H*4/5, W, H/5);
  rect(0.67*W, 0, 2/5*W, H);

  let xstop = W/15;
  let ystop = diff = H/16;
  let names = ["la", "ma", "θa","lb", "mb", "θb"];
  let units = ['pxs', 'kg', 'rad','pxs', 'kg', 'rad'];
  fill(255);
  strokeWeight(0);
  textSize(10);
  for (let i = 0; i<names.length; i++) {
    if (i == 3) {ystop = diff; xstop+=W*0.28};
    text(names[i]+"/"+units[i], xstop-W/20, ystop+H/100);
    text(sliders[names[i]].value(), xstop-W/20+140, ystop+H/100);
    ystop+=diff;
  };
  text("Spring length/pxs:"+ sliders.li.value(),W/25, 0.85*H);
  text("nskip: "+nskip,0.232*W, 0.85*H);
  text("dt/s: "+dt,0.41*W, 0.85*H);
  stroke(255);
  makeAxis(0.73*W, 0.40*H, 0.2*W, 0.28*H, "x", "y");
  makeAxis(0.73*W, 0.85*H, 0.2*W, 0.28*H, "x", "y");

  //Making the pendulum support
  strokeWeight(3);
  line(W*0.1, H*0.32, W*0.55, H*0.32);

  //Dashed line
  stroke(50);
  dashLine(W*0.2, H*0.33, 5, 3, 10, "y");
  dashLine(W*0.2+separation, H*0.33, 5, 3, 10, "y");
};

function updateValues(){
  li = sliders.li.value();
  la = sliders.la.value();
  lb = sliders.lb.value();
  ma = sliders.ma.value();
  mb = sliders.mb.value();
  θa = sliders.θa.value();
  θb = sliders.θb.value();
  xa = la*sin(θa); xb = lb*sin(θb)+separation;
  ya = la*cos(θa); yb = lb*cos(θb);
  va = vb = 0;
  updated = true;
};

function setup() {
  setDefaults();
  canvas = createCanvas(W, H);

  //Button containers
  background(20);
  fill(50);
  stroke(70);
  strokeWeight(2);
  rect(0, 0, W, H/4);
  rect(0, H*4/5, W, H/5);
  rect(0.67*W, 0, 2/5*W, H);

  //Widgets - Sliders
  sliders.li = createSlider(10, separation*2, separation, 1);
  sliders.la = createSlider(0, 300, 150, 1);
  sliders.lb = createSlider(0, 300, 150, 1);
  sliders.ma = createSlider(0.1, 5, 1, 0.1);
  sliders.mb = createSlider(0.1, 5, 1, 0.1);
  sliders.θa = createSlider(0.01, 3.14/2, 3.14/4, 0.01);
  sliders.θb = createSlider(0.01, 3.14/2, 3.14/4, 0.01);

  //postioning the sliders
  let xstop = W/15;
  let ystop = diff = H/16;
  let names = ["la", "ma", "θa","lb", "mb", "θb"];
  let units = ['pxs', 'kg', 'rad','pxs', 'kg', 'rad'];
  fill(255);
  strokeWeight(0);
  textSize(10);
  for (let i = 0; i<names.length; i++) {
    if (i == 3) {ystop = diff; xstop+=W*0.28};
    let slider = sliders[names[i]];
    slider.position(xstop, ystop-H/40);
    slider.style('width', '100px');
    slider.mouseReleased(function(){updated=false;});
    text(names[i]+"/"+units[i], xstop-W/20, ystop+H/100);
    text(slider.value(), xstop-W/20+140, ystop+H/100);
    ystop+=diff;
  };

  //Making the slider on the bottom
  text("Spring length/pxs",W/25, 0.85*H);
  sliders.li.style('width', '100px');
  sliders.li.position(W/25, 13/15*H);
  sliders.li.mouseReleased(function(){updated=false;});

  //Time for the entries
  text("nskip",0.232*W, 0.85*H);
  entries.nskip = createInput("dt", "number");
  entries.nskip.size(80,15);
  entries.nskip.position(0.232*W, 13/15*H);
  entries.nskip.input(function(){nskip = Number(entries.nskip.value()).toFixed(0)})

  text("dt/s",0.41*W, 0.85*H);
  entries.dt = createInput("dt", "number");
  entries.dt.size(80,15);
  entries.dt.position(0.41*W, 13/15*H);
  entries.dt.input(function(){dt = Number(entries.dt.value())});

  stroke(255);
  makeAxis(0.73*W, 0.40*H, 0.2*W, 0.28*H, "x", "y");
  makeAxis(0.73*W, 0.85*H, 0.2*W, 0.28*H, "x", "y");

  //Making the pendulum support
  strokeWeight(3);
  line(W*0.1, H*0.32, W*0.55, H*0.32);

  //Dashed line
  stroke(50);
  dashLine(W*0.2, H*0.33, 5, 3, 10, "y");
  dashLine(W*0.2+separation, H*0.33, 5, 3, 10, "y");
};


function draw() {
  if (updated == false){updateValues()};
  resetBg();

  //Drawing moving objects
  translate(W*0.2, H*0.33);
  fill(60, 60, 250);
  stroke(240, 240, 250);
  line(0, 0, xa, ya);
  line(separation, 0, xb, yb);
  line(xa, ya, xb, yb);
  stroke(250, 250, 250);
  ellipse(xa, ya, ma*30, ma*30);
  ellipse(xb, yb, mb*30, mb*30);

  let i = nskip;
  while (i--){
    L = sqrt((xa-xb)**2+(ya-yb)**2);
    ga = -9.81*sin(θa), gb = -9.81*sin(θb);
    aa = -k*(li-L)/ma/L*((xb-xa)*cos(abs(θa))-(yb-ya)*sin(abs(θa)));
    va-=(ga+aa)*dt;
    vb-=(gb-aa/mb*ma)*dt;
    θa-=va*dt/la;
    θb-=vb*dt/lb;
    xa = la*sin(θa);
    ya = la*cos(θa);
    xb = separation+lb*sin(θb);
    yb = lb*cos(θb);
  };
  //Just to show frame rate
  fill(250);
  strokeWeight(0);
  text(frameRate().toFixed(0), -80, 170);

};
