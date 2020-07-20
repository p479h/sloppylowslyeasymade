let slider; //Slider
let theta; //angle
let LOF = 60;//Length of indicator line
let H = 400; //height of canvas
let W = 600; //Width of canvas
let bg = 255;//Background color
let colorData = [];//Color of the dots
let velData = []; //Data on velocity
let pathData = [];//Position in shape NxL where N is num dims
let vx; //Velocity along x
let vy; //Velocity along y
let x0=0; //Initial x for each round
let y0=H; //Initial y for each round
let t = [];//Time data
let dt;//Interval between calculations
let dtFlag;
let vx0 = 0;
let vy0=0;
let g = [0,9.81];//Acceletation of g.
let initv = 80//Initial speed
let thetaFlag; //Will represent the previous theta...
let dataFlag = true;//Set to false when no data collection is needed


function setup(){
  createCanvas(W, H);
  background(bg);
  slider = createSlider(0, 3.14/2, 1.5, 0.01); //For the angle
  slider.position(10, 10);
  slider.style('width', '90px');
  slider2 = createSlider(0.01, 1, 0.5, 0.01); //For dt
  slider2.style('width', '90px');
  slider2.position(140, 10);
  dt = slider2.value().toFixed(3);
  dtFlag = dt;
  theta = slider.value();
  thetaFlag = 100;//No just triggers a function
  textSize(10);
};

function draw(){
  //Setting up line
  background(bg);
  theta = slider.value();
  dt = slider2.value();
  line(0, H, LOF*cos(theta), H-LOF*sin(theta));

  //Setting up text
  fill(0, 102, 153)
  text((theta*360/(2*PI)).toFixed(2), 90, 40)
  text("Angle in degrees:", 10, 40)

  text("dt in seconds:", 140, 40);
  text(slider2.value().toFixed(2), 203, 40);


  //Plotting data!!!
  if (theta!=thetaFlag || dt!=dtFlag){
    clearValues();
    genData();
    thetaFlag = theta;
  };
  for (let i = 0; i<pathData.length; i++){
    fill(colorData[i]);
    ellipse(pathData[i][0], pathData[i][1], 5, 5)};
}

function genData(){
  theta = slider.value();
  vx = initv*cos(theta);
  vy = -initv*sin(theta); //Negative sign due to inverted coo
  for (let i=0; true; i++){
    pathData.push([x0,y0]);
    velData.push([vx, vy]);
    x0+=vx*dt;
    y0+=(vy+vy0)/2*dt;
    vx0 = vx;
    vy0 = vy;
    vx+=g[0]*dt;
    vy+=g[1]*dt;
    if (vx**2+vy**2>initv**2){
      break;//Breaks when potential energy is exausted.
    };
  };
  let tempx = findMaxMin(velData.map(function(v){return v[0]}));
  let tempy = findMaxMin(velData.map(function(v){return v[1]}));
  for (let i = 0; i<velData.length; i++){
    let r = theNormalizer(tempx[0], tempx[1], velData[i][0]);
    let b = theNormalizer(tempy[0], tempy[1], velData[i][1]);
    colorData.push([r*254, 0, b*254])
    };
};

function theNormalizer(min, max, val){
  if (max==min){
    return(1)};
  return (val-min)/(max - min);
};

function findMaxMin(data){
  let min = data[0];
  let max = data[0];
  for (let i = 0; i<data.length; i ++){
    if (data[i]>max){max = data[i]}
    else if (data[i]<min){min = data[i]};
  };
  return [min, max];
};

function clearValues(){
  x0 = 0;
  y0 = H;
  vx = 0;
  vy = 0;
  velData = [];
  pathData = [];
  colorData = [];
};
