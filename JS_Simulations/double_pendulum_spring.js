//First the params of the pendulums
let θa, dθa, θb, dθb, ma, mb, xa, ya, xb, yb, la, lb, va, vb, ekmaxa, ekmaxb, eka, ekb, ekaData, ekbData;
let separation; //Distance between pivots

//Ohter params
let nskip, t, dt, g, updated, tData;

//Then the params of the spring
let li, L, k;

//Drawing elements
let W, H, bg, font, canvas, ax1, ax2;

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
  k: null,
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
  ekmaxa = ekmaxb=eka=ekb = 0;

  //Parameters of the spring
  li = separation;
  L = sqrt((xa-xb)**2+(ya-yb)**2);
  k=0.1;

  //Other parameters
  nskip = 550;
  dt = 0.0005;
  t = 0;
  g = 9.8;
  ekaData = ekbData = tData = [];
  updated = false;
};

function drawSpring(p1, p2,n){
  p1[0] += ma*15;//Account for size of mass
  p2[0] -= mb*15;
  let s = (p2[0] - p1[0])/(n-1);
  let x = [p1[0], p1[0]+s];
  let yrat = (p2[1] - p1[1])/n;
  let y = [p1[1], p1[1]+yrat];
  for (let i = 2; i<n-1; i++){
    x[i] = p1[0]+(i-0.5)*s;
    y[i] = p1[1]+ ((i%2 == 0)? (i-1)*yrat-10:(i-1)*yrat+10);
  };
  x[x.length] = p2[0]-s;
  x[x.length] = p2[0]-0.2*s;
  y[y.length] = p2[1]-2*yrat;
  y[y.length] = p2[1]-yrat;
  strokeWeight(2);
  stroke(255);
  for (let i=1; i<x.length; i++){
    line(x[i-1], y[i-1], x[i], y[i]);
  };
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
  let units = ['m', 'kg', 'rad','m', 'kg', 'rad'];
  fill(255);
  strokeWeight(0);
  textSize(10);
  for (let i = 0; i<names.length; i++) {
    if (i == 3) {ystop = diff; xstop+=W*0.28};
    text(names[i]+"/"+units[i], xstop-W/20, ystop+H/100);
    text(sliders[names[i]].value(), xstop-W/20+140, ystop+H/100);
    ystop+=diff;
  };
  text("Spring length/m:"+ sliders.li.value(),W/25, 0.84*H);
  text("Spring k/Nm-1: "+ sliders.k.value(),W/25, 0.93*H);
  text("nskip: "+nskip,0.232*W, 0.85*H);
  text("dt/s: "+dt,0.41*W, 0.85*H);
  stroke(255);

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
  k = sliders.k.value();
  xa = la*sin(θa); xb = lb*sin(θb)+separation;
  ya = la*cos(θa); yb = lb*cos(θb);
  va = vb = 0;
  eka = ekb = ekmaxa = ekmaxb = 0;
  ekaData = [];
  ekbData = [];
  tData = [];
  t = 0;
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
  sliders.k = createSlider(0.01, 2, 0.1, 0.01);

  //postioning the sliders
  let xstop = W/15;
  let ystop = diff = H/16;
  let names = ["la", "ma", "θa","lb", "mb", "θb"];
  let units = ['m', 'kg', 'rad','m', 'kg', 'rad'];
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
  text("Spring length/m",W/25, 0.85*H);
  sliders.li.style('width', '100px');
  sliders.li.position(W/25, 0.85*H);
  sliders.li.mouseReleased(function(){updated=false;});

  //Kslider
  text("Spring k/Nm-1",W/25, 0.85*H);
  sliders.k.style('width', '100px');
  sliders.k.position(W/25, 0.94*H);
  sliders.k.mouseReleased(function(){updated=false;});

  //Time for the entries
  text("nskip",0.232*W, 0.85*H);
  entries.nskip = createInput("dt", "number");
  entries.nskip.size(80,15);
  entries.nskip.position(0.232*W, 13/15*H);
  entries.nskip.input(function(){nskip = Number(entries.nskip.value()).toFixed(0);updated = false})

  text("dt/s",0.41*W, 0.85*H);
  entries.dt = createInput("dt", "number");
  entries.dt.size(80,15);
  entries.dt.position(0.41*W, 13/15*H);
  entries.dt.input(function(){dt = Number(entries.dt.value()); updated = false});

  ax1= new makeAxis(0.72*W, 0.45*H, 0.25*W, 0.35*H,                      n=4, xlim = [0, 10],ylim = [0, 10],
                    xlabel = 't / s', ylabel = 'eka / J');
  ax2= new makeAxis(0.72*W, 0.9*H, 0.25*W, 0.28*H, n=4,
    xlim = [0, 10],ylim = [0, 10],xlabel = 't / s', ylabel = 'ekb / J');

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

  //Updating limits
  ax1.xlim = [tData[0], t];
  ax2.xlim = [tData[0], t];

  ax1.ylim = [0, ekmaxa];
  ax2.ylim = [0, ekmaxb];


  if (ekaData.length>100){
    ekaData.shift();
    ekbData.shift();
    tData.shift();
  };

  stroke(255, 255, 255,250);
  strokeWeight(1);

  //Making the spines and arrows
  ax1.construct();
  ax2.construct();
  stroke(255);
  fill(255);

  //Drawing xticks
  textSize(9);
  ax1.xticks();
  ax2.xticks();

  //Drawing yticks
  ax1.yticks();
  ax2.yticks();

  ax1.plot(tData, ekaData, relsize = 5, marker = 'o');
  ax2.plot(tData, ekbData, relsize = 5, marker = '-');

  translate(W*0.2, H*0.33);

  strokeWeight(0.5);
  fill(10, 10, 250,150);

  //Drawing tha angle showers
  if (sin(θa)>0){
    arc(0, 0, la/2, la/2, -θa+3.14/2, 3.14/2);
  } else {arc(0, 0, la/2, la/2,3.14/2,-θa+3.14/2);}

  if (sin(θb)>0){
    arc(separation, 0, lb/2, lb/2, -θb+3.14/2, 3.14/2);
  } else {arc(separation, 0, lb/2, lb/2,3.14/2,-θb+3.14/2);
         };

  //Text
  textSize(13);
  strokeWeight(0.5);
  fill([223, 249, 218]);
  text("θa: "+ θa.toFixed(3), la*sin(θa/2)/3, la*cos(θa/2)/3);

  text("θb: "+ θb.toFixed(3), lb*sin(θb/2)/3+separation, lb*cos(θb/2)/3);
  textSize(14);

  //Drawing moving objects
  fill(60, 60, 250);
  stroke(240, 240, 250);
  strokeWeight(3);
  line(0, 0, xa, ya);
  line(separation, 0, xb, yb);
  //line(xa, ya, xb, yb);
  drawSpring([xa, ya], [xb, yb],10);
  stroke(250, 250, 250);
  ellipse(xa, ya, ma*30, ma*30);
  ellipse(xb, yb, mb*30, mb*30);

  //Computations to evolve system
  let i = nskip;
  while (i--){
    L = sqrt((xa-xb)**2+(ya-yb)**2);
    ga = -9.81*sin(θa), gb = -9.81*sin(θb);
    aa = -k*(li-L)/ma/L*((xb-xa)*cos(θa)-(yb-ya)*sin(θa));
    ab = -k*(li-L)/mb/L*((xb-xa)*cos(θb)-(yb-ya)*sin(θb));
    va-=(ga+aa)*dt;
    vb-=(gb-ab)*dt;
    θa-=va*dt/la;
    θb-=vb*dt/lb;
    xa = la*sin(θa);
    ya = la*cos(θa);
    xb = separation+lb*sin(θb);
    yb = lb*cos(θb);
    t+=dt;
  };
  //Kinetic energy
  eka = 1/2*ma*va**2;
  ekb = 1/2*mb*vb**2;
  if (eka>ekmaxa){ekmaxa = eka};
  if (ekb>ekmaxb){ekmaxb = ekb};
  ekaData.push(eka);
  ekbData.push(ekb);
  tData.push(t);

  //Just to show frame rate
  fill(250);
  strokeWeight(0);
  text("FPS:"+frameRate().toFixed(0), -110, 170);
};


//TestPhase!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
function makeAxis(x, y, w, h, n=5,
                  xlim = [0, 10],
                  ylim = [0, 10],
                  xlabel = '',
                  ylabel = ''){
  let self = this;
  self.x = x;
  self.y = y;
  self.w = w;
  self.h = h;
  self.n = n;
  self.ticklen = sqrt(w**2+h**2)/30
  self.xlim = xlim;
  self.ylim = ylim;
  self.xlabel = xlabel;
  self.ylabel = ylabel;
  self.construct = function construct(){
    let x = self.x;
    let y = self.y;
    let w = self.w;
    let h = self.h;
    let arrowlen = sqrt(w**2+h**2)/50
    let xlabel = self.xlabel;
    let ylabel = self.ylabel;
    strokeWeight(3);
    textSize(12);

    //Making the spines
    line(x, y, x+w, y);
    line(x, y, x, y-h);

    //Arrows
    triangle(x+w, y+arrowlen, x+w, y-arrowlen, x+w+arrowlen*1.5, y);
    triangle(x-arrowlen, y-h, x+arrowlen, y-h, x, y-h-arrowlen*1.5);

    //Labels
    strokeWeight(0);
    textSize(14);

    text(xlabel, x+w*0.9, y+5*arrowlen);
    text(ylabel, x-7*arrowlen, y-h*1.1);
  };

  //Xticks function
  self.xticks = function xticks(){
    let xsep = self.w/(self.n+1);
    textAlign(CENTER);
    for (let i = 1; i<=self.n; i++){
      let x = self.x+i*xsep;
      let transx = ((x-self.x)/self.w*(self.xlim[1]-self.xlim[0])).toFixed(1);
      strokeWeight(1);
      line(x, self.y-self.ticklen, x, self.y);
      strokeWeight(0);
      text((Number(transx)+self.xlim[0]).toFixed(1),x, self.y+2*self.ticklen);
    };
    textAlign(LEFT);
  };

  //Yticks function
  self.yticks = function yticks(){
    let ysep = self.h/(self.n+1);
    textAlign(RIGHT);
    for (let i = 1; i<=self.n; i++){
      let y = self.y-self.h+i*ysep;
      let transy = (-(y-self.y)/self.h*(self.ylim[1]-self.ylim[0])).toFixed(1);
      strokeWeight(1);
      line(self.x, y, self.x+self.ticklen, y);
      strokeWeight(0);
      text(transy,self.x-self.ticklen, y);
    };
    textAlign(LEFT);
  };

  //Returns array with the actual pixel positions of array;
  self.xtransform = function xtransform(arr){
    let Max = self.xlim[1] , Min= self.xlim[0];
    let diff = Max-Min;
    let arrRet = [];
    for (let i =0; i<arr.length; i++){
      arrRet[i] = self.x+(arr[i]-Min)*self.w/(diff);
    };
    return arrRet;
  };

  //Returns array with the actual pixel positions of array;
  self.ytransform = function ytransform(arr){
    let Max = self.ylim[1], Min= self.ylim[0];
    let diff = Max-Min;
    let arrRet = [];
    for (let i =0; i<arr.length; i++){
      arrRet[i] = self.y-(arr[i]-Min)*self.h/(diff);
    };
    return arrRet;
  };

  //plots data in the order it is provided
  //'o' is ball, 's' is size, '-' is line,
  self.plot = function plot(xarr, yarr, relsize=20, marker='o'){
    let transx = self.xtransform(xarr);
    let transy = self.ytransform(yarr);
    if (marker == 'o') {
      for (let i = 0; i<transx.length; i++){
        ellipse(transx[i], transy[i], relsize, relsize);
      };
    }
    else if (marker == '-'){
      strokeWeight(3);
      if (xarr.length>=1){
        for (let i = 1; i<transx.length; i++){
          line(transx[i-1], self.y, transx[i], transy[i]);
      };
    };
  };
};
};
