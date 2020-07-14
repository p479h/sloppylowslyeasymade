//First the constants and other values
let Ø; //Angle between vertical and string. Torwards x ax is positive
let dØ; //Infinitesimal change in angle
let t; //Time since beggining of the simulation
let dt; //Time step
let x; //X coord, which will be updated if the thingy moves!
let y; //y coord, which will be updated if the thingy moves!
let v; //SPEED not velocity
let F; //The external force on the mass (gravity)
let l; //Length of the spring
let m; //Mass of the object
let runFlag; //Controls whether time is allowed to pass or not.

//Now onto the widgets
let W; //Canvas width
let H; //Canvas height
let sldt; //Slider for dt
let slLen; //Slider length of spring
let slM; //Slider mass of the object
let slØ; //SLider angle
let startBut; //Start animation button
let replBut; //Button to reposition elements
let pauseBut; //Stop the animation at a given time
let xSLI; //X position of sliders
let canvas; //Canvas in case a canvas "instance" is returned
let bg; //Background color [r,g,b]
let fontColor; //Color fo the font


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
};

/*Now we make a callback generator for the widgets
This is made in an entirely separate function due to
organization purpuses.

The input is the name of the widget. It returns a function
that performs the action the widget is to do.*/
function callback(widName){
  let s = widName
  if (s == "sldt"){
    return function(){dt = sldt.value();};
  }
  else if (s == "slM"){
    return function(){m = slM.value();};
  }
  else if (s == "slLen"){
    return function(){l = slLen.value();};
  }
  else if (s == "slØ"){
    return function(){Ø = slØ.value();};
  }
  else if (s == "startBut"){
    return function(){runFlag = true};
  }
  else if (s == "pauseBut"){
    return function(){runFlag = false};
  }
  else if (s == "replBut"){
    return function(){resetValues();};
  }
  else{
    alert("UNRECOGNIZED WIDZgEt");
  }
};


/*Now we make a function to attribute values to the
constants above when used the first time.
Else, it resets everything to initial situation.*/
function setup() {
  //Check if the funcition is being used for first time
  if (sldt == undefined || sldt == null) {
    //Making the canvas
    W = 500;
    H = 400;
    canvas = createCanvas(W, H);
    bg = [0, 0, 0];
    background(bg);

    //Improves the looks
    smooth();

    //Setting the x position of left corner of sliders
    xSLI = 10;

    //Setting fontcolor
    fontColor = [200, 255, 255, 255];
    fill(fontColor);
    textSize(14);
    textFont("Consolas")

    //Dt slider first
    sldt = createSlider(0.001, 1, 0.001, 0.001);
    sldt.position(10, 10);
    sldt.style('width', '80px');

    //Then make the chord length slider
    slLen = createSlider(10, 300, 200, 1);
    slLen.position(xSLI, 40);
    slLen.style('width', '80px');

    //Then make the slider with the mass
    slM = createSlider(0.1, 200, 100, 1);
    slM.position(xSLI, 70);
    slM.style('width', '80px');

    //Make the Ø slider
    slØ = createSlider(0, PI / 2, PI / 4, 0.01);
    slØ.position(xSLI, 100);
    slØ.style('width', '80px');



  };
  //With the sliders in place we can set the initial values
  resetValues();
};

function draw() {
  //Resetting constants
  dt = sldt.value();
  m = slM.value();
  l = slLen.value();
  x = l*sin(Ø);
  y = l*cos(Ø);

  //Resetting background
  background(bg);
  //Redrawing text
  fill(fontColor);
  noStroke();
  text("dt: "+dt+" s",xSLI+90, 10+15);
  text("l: "+l+" pxs",xSLI+90, 40+15);
  text("Ø: "+slØ.value()+" rad",xSLI+90, 100+15);
  text("M: "+m+" kg",xSLI+90, 70+15);

  text("t: "+t.toFixed(2)+" s",xSLI+200, 10+15);
  text("T: "+(2*PI*(l/F)**0.5).toFixed(2)+" s",xSLI+200, 40+15);

  //Arc with angle
  translate(W/2, H/5);
  noFill();
  textSize(18);
  stroke([255, 255, 255, 200]);
  strokeWeight(2);
  fill([200, 249, 200, 200]);
  if (Ø>0){
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


  strokeWeight(2)
  //Drawing mass
  fill([50, 249, 50]);
  stroke([255, 255, 255])
  ellipse(x, y, m/5, m/5);
  if (runFlag == true){
    v -= F*sin(Ø)*dt
    Ø += v*dt/l;
    t += dt
  };
  };
