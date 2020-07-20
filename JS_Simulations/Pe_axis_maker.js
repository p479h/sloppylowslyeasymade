/*This file contains a function that allows you to make a simple plot
Example on how to use it:

ax = new makeAxis(); //Create an axis object!
ax.param = <param of your choice>//Option used to costumize plot elements.
//Not all elements work yet

now onto the actual showing of the plot:
To show the spines:
ax.construct();

To show the x and y ticks with tickLabels:
ax.yticks();
ax.xticks();

You can find ouy more by playing with the following example:


function setup(){createCanvas(W, H);
                rect(0,0,W, H);
                ax = new makeAxis(0.2*W, 0.85*H, 0.5*W, 0.5*H);
                ax.style = "clear";};
                // ax.ylim = [10, 20];};

function draw(){
  background(255);
  ax.drawBg();
  ax.construct();
  ax.xticks();
  ax.yticks();
  ax.plot([1,5], [1,8], relsize=10, marker = 'o');
};
*/

function makeAxis(x, y, w, h, n=5,
                  xlim = [0, 10],
                  ylim = [0, 10],
                  xlabel = 'x',
                  ylabel = 'y',
                  xLabelSize = 15,
                  yLabelSize = 15,
                  style = 'dark',
                  strokew = 3,
                  bg = 0,
                  tickLabelSize = 12,
                  font = "Consolas",
                  sigFig = 0,){
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
  self.style = style;
  self.bg = bg;//background color
  self.strokew = strokew;//Color of lines and text
  self.tickLabelSize = tickLabelSize; // size of text
  self.xLabelSize = xLabelSize;
  self.yLabelSize = yLabelSize;
  self.font = font;
  self.sigFig = sigFig; //Significant figures
  self.construct = function construct(){
    let x = self.x;
    let y = self.y;
    let w = self.w;
    let h = self.h;
    let arrowlen = sqrt(w**2+h**2)/50
    let xlabel = self.xlabel;
    let ylabel = self.ylabel;

    if (self.style == 'dark'){stroke(255);fill(255);}             else{stroke(0);fill(0);};
    strokeWeight(self.strokew);
    textSize(self.tickLabelSize);

    //Making the spines
    line(x, y, x+w, y);
    line(x, y, x, y-h);

    //Arrows
    triangle(x+w, y+arrowlen, x+w, y-arrowlen, x+w+arrowlen*1.5, y);
    triangle(x-arrowlen, y-h, x+arrowlen, y-h, x, y-h-arrowlen*1.5);

    //Labels
    textFont(self.font);
    strokeWeight(0);
    textSize(self.xLabelSize);
    text(xlabel, x+w, y+5*arrowlen);
    textSize(self.yLabelSize);
    text(ylabel, x-4*arrowlen, y-h*1.1);
  };


  //Draws a rectangle underneath the plot for better
    //contrast. It is not really a good function but it
    //can help a little.
  self.drawBg = function drawBg(){
    strokeWeight(1);
    if (self.style == 'dark'){
      fill(0);stroke(255)}else{fill(255);stroke(0)};
    (self.style == 'dark')? fill(0):fill(250);
    rect(self.x-self.w*0.2, self.y+self.h*0.2, self.w*1.3, -self.h*1.4);
  };

  //Xticks function
  self.xticks = function xticks(){
    let xsep = self.w/(self.n+1);
    textAlign(CENTER);
    textFont(self.font);
    for (let i = 1; i<=self.n; i++){
      let x = self.x+i*xsep;
      let transx = ((x-self.x)/self.w*(self.xlim[1]-self.xlim[0])).toFixed(1);
      strokeWeight(1);
      line(x, self.y-self.ticklen, x, self.y);
      strokeWeight(0);
      text((Number(transx)+self.xlim[0]).toFixed(self.sigFig),x, self.y+2*self.ticklen);
    };
    textAlign(LEFT);
  };

  //Yticks function
  self.yticks = function yticks(){
    let ysep = self.h/(self.n+1);
    textAlign(RIGHT);
    textFont(self.font);
    for (let i = 1; i<=self.n; i++){
      let y = self.y-self.h+i*ysep;
      let transy = -(y-self.y)/self.h*(self.ylim[1]-self.ylim[0]);
      strokeWeight(1);
      line(self.x, y, self.x+self.ticklen, y);
      strokeWeight(0);
      text((Number(transy)+self.ylim[0]).toFixed(self.sigFig),self.x-self.ticklen, y);
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
          line(transx[i-1], transy[i-1], transx[i], transy[i]);
      };
    };
  };
};
};
