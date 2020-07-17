//First the constants and other values
let Ø, dØ, t, dt, F, x, y, v, l, m; //Parms and dummy vars
let Emax; //For the graphs
let runFlag; //Flag to check if simulation runs
let data = {
  Ødata : [],
  tdata : [],
  EPdata: [],
  EKdata: [],
};

//Now onto the widgets
let W = 500, H = 400; //Canvas height and width
let sldt,slLen, slM, slØ; //Sliders
let startBut,replBut,pauseBut; //Buttons
let xSLI; //X position of sliders
let canvas; //Canvas in case a canvas "instance" is returned
let bg = [0, 0, 0]; //Background color [r,g,b]
let fontColor = [10, 10, 10, 255]; //Color fo the font

function resetValues(){
  //THis function resets constants to default
  slØ.value(3.14/ 4);
  sldt.value(0.09);
  slM.value(150);
  slLen.value(200);
  bg = [0, 0, 0];
  Ø = slØ.value();
  dt = sldt.value();
  m = slM.value();
  l = slLen.value();
  t = 0;
  F = 9.8;
  runFlag = true;
  x = l * sin(Ø);
  y = l * cos(Ø);
  v=0; //SPeeed not velocity
  W = 500;
  H = 400;
  Emax = l*(1-cos(Ø))*F*m/70; //Just for scaling.
};

/*Now we make a function to attribute values to the
constants above when used the first time.
Else, it resets everything to initial situation.*/
function setup() {
  //Check if the funcition is being used for first time
  if (sldt == undefined || sldt == null) {
    //Making the canvas
    canvas = createCanvas(W, H);
    background(bg);

    //Improves the looks
    smooth();

    //Setting the x position of left corner of sliders
    xSLI = 10;

    //Setting fontcolor
    fill(fontColor);
    textSize(14);
    textFont("Consolas");

    //Dt slider first
    sldt = createSlider(0.001, 1, 0.001, 0.001);
    sldt.position(10, 10);
    sldt.style('width', '80px');

    //Then make the chord length slider
    slLen = createSlider(10, 300, 200, 1);
    slLen.position(xSLI, 36);
    slLen.style('width', '80px');

    //Then make the slider with the mass
    slM = createSlider(0.1, 200, 100, 1);
    slM.position(xSLI, 62);
    slM.style('width', '80px');

    //Make the Ø slider
    slØ = createSlider(0, PI / 2, PI / 4, 0.01);
    slØ.position(xSLI, 88);
    slØ.style('width', '80px');

    startBut = createButton("Begin");
    startBut.position(220, 10);
    startBut.mousePressed(
      function play(){
        v=0;
        Ø = slØ.value();
        runFlag = true;
      });

    pauseBut = createButton("Pause");
    pauseBut.position(220, 45);
    pauseBut.mousePressed(
      function pause(){
        runFlag = false;
      });

    replBut = createButton("Replay");
    replBut.position(220, 80);
    replBut.mousePressed(
      function replay(){
        resetValues();
      });

  };
  //With the sliders in place we can set the initial values
  resetValues();
};

function draw() {
  //Resetting background
  background(bg);

  //Drawing boxes
  fill(192,192,192)
  rect(0,0,W/1.6, H/3.5);

  //Resetting constants
  dt = sldt.value();
  m = slM.value();
  l = slLen.value();
  x = l*sin(Ø);
  y = l*cos(Ø);

  //Redrawing text
  fill(fontColor);
  noStroke();
  text("dt: "+dt+" s",xSLI+90, 8+15);
  text("l: "+l+" pxs",xSLI+90, 35+15);
  text("Ø: "+slØ.value()+" rad",xSLI+90, 85+15);
  text("M: "+m+" kg",xSLI+90, 60+15);

  //time label
  textSize(17);
  fill(255);
  text("t: "+t.toFixed(2)+" s",xSLI+320, 10+15);
  text("EK: "+(0.5*m*v**2).toFixed(0)+" J",xSLI+320, 37+15);
  text("EP: "+(m*l*(1-cos(Ø))*F).toFixed(0)+" J",xSLI+320, 65+15);
  text("EK+EP: "+(0.5*m*v**2+m*l*(1-cos(Ø))*F).toFixed(0)+" J",xSLI+320, 92+15);

  //Arc with angle
  translate(W/3, H/3);
  noFill();
  textSize(18);
  stroke([255, 255, 255, 200]);
  strokeWeight(2);
  fill([200, 249, 200, 200]);
  if (sin(Ø)>0){
    arc(0, 0, l/2, l/2, -Ø+3.14/2, 3.14/2);
  } else {arc(0, 0, l/2, l/2,3.14/2,-Ø+3.14/2);}

  strokeWeight(0.5);
  fill([123, 249, 148]);
  text("Ø", l*sin(Ø/2)/3, l*cos(Ø/2)/3);
  fill([223, 249, 218]);
  textSize(15);
  text("("+String(Ø.toFixed(3))+")", l*sin(Ø/2)/3+40, l*cos(Ø/2)/3);
  textSize(14);

  //Drawing line
  strokeWeight(5)
  stroke([40, 40, 200]);
  line(0, 0, x, y);
  stroke(255, 255, 255);
  line(-20, 0, 20, 0);
  stroke([255, 255, 255, 250]);
  strokeWeight(2);
  line(0, 0, 0, l/20);
  line(0, 2*l/20, 0, 3*l/20);
  line(0, 4*l/20, 0, 5*l/20);
  line(0, 6*l/20, 0, 7*l/20);

  makeAxis(170, 90, 105, 85, "t", "E");
  strokeWeight(2);
  makeAxis(170, 210, 105, 85, "t", "Ø");
  textSize(13);
  strokeWeight(2);

  strokeWeight(2)
  //Drawing mass
  fill([50, 249, 50]);
  stroke([255, 255, 255])
  ellipse(x, y, m/5, m/5);
  if (runFlag == true){
    v -= F*sin(Ø)*dt
    Ø += v*dt/l;
    t += dt;
    ellipse(300, -87, 10, 10);
    ellipse(200, -(0.5*m*v**2)/Emax+70, 10, 10);

    fill([250, 49, 50]);
    ellipse(300, -59, 10, 10);
    ellipse(220, -(m*l*(1-cos(Ø))*F)/Emax+70, 10, 10);

    fill([50, 49, 250]);
    ellipse(300, -32, 10, 10);
    ellipse(250,-(m*l*(1-cos(Ø))*F+0.5*m*v**2)/Emax+70, 10, 10);
    fill([250, 249, 250]);
    ellipse(220, Ø*50+160, 10, 10);
  };

};

function makeAxis(x, y, w, h, xlabel, ylabel){
  line(x, y, x+w, y);
  line(x, y, x, y-h);
  triangle(x+w, y+h/20, x+w, y-h/20, x+w+w/20, y);
  triangle(x-w/20, y-h, x+w/20, y-h, x, y-h-h/20);
  textSize(10);
  strokeWeight(0.1);
  text(xlabel, x+0.9*w, y+h/4);
  text(ylabel, x-w/6, y-h*0.9);
};

function getMax(arr){
  //Get's maximun and minimun in array for normalization
  //purpuses
  let max, min;
  max = arr[0]; min = arr[0];
  for (let i=0; i<arr.length;i++){
    max = (arr[i]>max)? arr[i]:max;
    min = (arr[i]<min)? arr[i]:min;
  };
  max = (typeof max == "number")? max:arr[0];
  min = (typeof min == "number")? min:arr[0];
  return [min, max];
};

function normalize(arr, scale){
  let fictitious = []; //Dummy array
  maxmin = getMax(arr);
  Min = maxmin[0];
  Max = maxmin[1];
  if (Max-Min!=0){
    for (let i=0; i<arr.length;i++){
      fictitious.push((arr[i]-Min)*scale/(Max-Min))
    };
    return fictitious
    } else {
      return arr};
};
