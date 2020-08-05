let canvas, figure, axes;
let W = H = 400;

function setup() {
  canvas = createCanvas(W, H);

  plot = new makePlot(canvas);
  plot.build([0, 0, 300, 300]);

  plot.setAxLimits([0, 100], [0, 200]);
  let i = 0;
  canvas.background(250, 0, 0);
  plot.startLine([10, 100]);
  while (i++ < 1000) {
    plot.addLineTo([10 + i / 50, sin(i / 100) * 20 + 100]);
  };
  plot.display();


  setInterval(
    () => {
      plot.addLineTo([10 + i / 50, sin(i / 100) * 20 + 100]);
      plot.setAxLimits([i/50, i/50+20], [0, 200]);
      i++
      plot.display();
    }, 10);
};

function draw() {};


function makePlot(canvas) {
  //First let's declare some global variables for a plot
  //This is mainly for readibility
  let figure, axes, bbox;
  let contextPoint = this.contextPoint = [0, 0]; //Used for continuity!

  /*bbox = [x0, y0, x1, y1];
  x0 and y0 lie at the top left corner
  x1 and y1 lie at the bottom right corner
  Used for scaling and positioning*/
  this.xlim = [0, 100];
  this.ylim = [0, 100];

  this.build = (bbox) => {
    this.bbox = (arguments.length > 0) ? bbox : [0, 0, 0, 0];
    //Sets bbox for display later
    // pixelDensity(2); //Glitches in editor

    figure = createGraphics(300, 300);
    figure.context = figure.elt.getContext("2d");
    figure.bg = "rgba(0, 0, 0, 1)";
    figure.background(figure.bg);
    this.figure = figure;

    axes = createGraphics(500, 500);
    axes.context = axes.elt.getContext("2d");
    axes.bg = "rgba(255, 0, 0, 1)";
    axes.background(axes.bg);
    axes.context.imageSmoothingEnabled = false;
    figure.context.imageSmoothingEnabled = false;
    this.axes = axes;

    figure.context.save();
    axes.context.save();
  };

  this.display = () => {
    let ctx = canvas.elt.getContext("2d");
    ctx.save();

    this.figure.image(axes,
      this.figure.width / 10,
      this.figure.height / 10,
      this.figure.width * 0.8,
      this.figure.height * 0.8);

    image(this.figure,
      this.bbox[0], this.bbox[1],
      this.bbox[2] - this.bbox[0],
      this.bbox[3] - this.bbox[1]);
    ctx.restore();
  };

  this.setAxLimits = (xlim = [10, 100], ylim = [0, 100]) => {
    /*This is just a bunch of scaling and translating
    I never had linear algebra so I don't know the terms*/
    let xdist = xlim[1] - xlim[0];
    let ydist = ylim[1] - ylim[0];
    axes.context.restore();
    axes.context.save();
    axes.context.scale(axes.width / xdist, -axes.height / ydist);
    axes.context.translate(-xlim[0], -ydist);

    /*The comment is for TESTING in case a glitch is found*/
    //     axes.ellipse(50, 10, 5, 5);
    //     axes.fill(0, 250, 0);
    //     axes.ellipse(50, 20, 5, 5);

    //     axes.fill(0, 0, 0, 0);
    //     axes.rect(xlim[0]*1.1, ylim[0]*1.1, xdist*0.8, ydist*0.8)
    /*End of testing*/


    //Now we use the OLD lims to resize the current drawing
    //Negative signs are odd because of coordinate system
    axes.context.save();
    axes.scale(1, -1);

    axes.context.drawImage(axes.elt,
      this.xlim[0], -this.ylim[1],
      this.xlim[1] - this.xlim[0],
      this.ylim[1] - this.ylim[0]);
    axes.context.restore();

    //We also need to avoid ANNYING connections between old and new lines we draw
    axes.context.beginPath();
    axes.context.closePath();
    axes.context.moveTo(...this.contextPoint);

    //Now we don't need the old lims anymore
    this.xlim = xlim;
    this.ylim = ylim;
  };

  this.addLineTo = (arr) => {
    //Draws a line between the last drawn point and point
    axes.context.lineTo(...arr);
    axes.context.stroke();
    this.contextPoint = arr;
  };

  this.startLine = (arr) => {
    axes.context.moveTo(...arr);
  };

  this.plot = (arr) => {
    if (arr.length == 0) {
      return null;
    };
    axes.context.moveTo(...arr[0]);
    for (let Point in arr) {
      axes.context.lineTo(...Point);
    };
    axes.context.stroke();
  };
};
