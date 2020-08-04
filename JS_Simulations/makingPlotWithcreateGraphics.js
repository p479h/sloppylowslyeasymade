let canvas, figure, axes;
let W = H = 400;

function setup() {
  canvas = createCanvas(W, H);
  background(0, 0, 255);

  plot = new makePlot(canvas);
  plot.build([0, 0, 300, 300]);
  plot.display();

};

function draw() {
};


function makePlot(canvas){
  //First let's declare some global variables for a plot
  //This is mainly for readibility
  let figure, axes, bbox;

  pixelDensity(1);//Glitches in editor

  /*bbox = [x0, y0, x1, y1];
  x0 and y0 lie at the top left corner
  x1 and y1 lie at the bottom right corner
  Used for scaling and positioning*/
  this.xlim = [0, 100];
  this.ylim = [0, 100];

  this.build = (bbox) => {
    this.bbox = (arguments.length > 0)? bbox:[0, 0, 0, 0];
    //Sets bbox for display later

    figure = createGraphics(300, 300, canvas);
    figure.context = figure.elt.getContext("2d");
    figure.bg = "rgba(0, 0, 0, 1)";
    figure.background(figure.bg);
    this.figure = figure;
    console.log(this);

    axes = createGraphics(600, 600, figure);
    axes.context = axes.elt.getContext("2d");
    axes.bg = "rgba(255, 0, 0, 1)";
    axes.background(axes.bg);
    axes.elt.imageSmoothingEnabled =false;
    figure.elt.imageSmoothingEnabled =false;
    this.axes = axes;

  };

  this.display = () => {
    let ctx = canvas.elt.getContext("2d");
    let ctx2 = this.figure.context;
    let ctx3 = this.axes.context;
    ctx.save();
    ctx2.save();
    ctx3.save();
    ctx.resetTransform();
    ctx2.resetTransform();
    ctx3.resetTransform();

    this.figure.image(axes,
      this.figure.width / 10,
      this.figure.height / 10,
      this.figure.width * 0.8,
      this.figure.height * 0.8);

    console.log(this.bbox);
    image(this.figure,
      this.bbox[0], this.bbox[1],
      this.bbox[2] - this.bbox[0],
      this.bbox[3] - this.bbox[1]);
    ctx.restore();
    ctx2.restore();
    ctx3.restore();
  };

  this.setAxLimits = (xlim=[0, 100], ylim=[0, 100]) => {
    this.xlim = xlim; this.ylim = ylim;
    let xdist = xlim[1] - xlim[0];
    let ydist = ylim[1] - ylim[0];
    axes.context.resetTransform();
    axes.context.drawImage(axes.elt, 0, 0);
    axes.scale(axes.width / xdist, -axes.height / ydist);
    axes.translate(-xlim[0], -ydist);
  };

  this.addLineTo = (Point) => {
    //Draws a line between the last drawn point and point
    this.setAxLimits(this.xlim, this.ylim);
    axes.context.lineTo(...Point);
    axes.stroke();
  };

  this.startLine = (Point) => {
    this.setAxLimits(this.xlim, this.ylim);
    axes.context.moveTo(Point);
  };

  this.plot = (arr) => {
    if (arr.length == 0){return null};
    this.setAxLimits(this.xlim, this.ylim);
    axes.context.moveTo(...arr[0]);
    for (let Point in arr){
      axes.context.lineTo(...Point);
    };
    axes.context.stroke();
  };
};
