{//Brackets to avoig conflicting scopes
  let canvas = document.getElementById("pythagoreanSVG");
  let rect = canvas.children[0];
  let lines = document.getElementsByClassName("dashedLines")[0].children;
  let circles = document.getElementsByClassName("movableCircles")[0].children;
  let texts = document.getElementsByClassName("movableCirclesText")[0].children;
  let b1Text = texts[0];
  let b2Text = texts[1];
  let line_Text = texts[2];
  let textΔx = texts[3];
  let textΔy = texts[4];
  let line_ = lines[0];
  let linex = lines[1];
  let liney = lines[2];
  let b1 = circles[0];
  let b2 = circles[1];
  line_.style.transition = "opacity 1.5s";
  b1.style.cursor = b2.style.cursor = "grab";
  b1.style.transition = b2.style.transition= "cursor .2s";
  let selectedBall = false;
  function moveBall(event){
    if (!selectedBall){return null;};
    b1.style.cursor = b2.style.cursor= "grabbing";

    selectedBall.setAttribute("cx", event.offsetX);
    selectedBall.setAttribute("cy", event.offsetY);

    let b1x = b1.cx.animVal.value;
    let b1y = b1.cy.animVal.value;
    let b2x = b2.cx.animVal.value;
    let b2y = b2.cy.animVal.value;

    line_.setAttribute("x1", b1x);
    line_.setAttribute("x2", b2x);
    line_.setAttribute("y1", b1y);
    line_.setAttribute("y2", b2y);
    line_.style.opacity = "0";

    linex.setAttribute("x1", b1x);
    linex.setAttribute("x2", b2x);
    linex.setAttribute("y1", b1y);
    linex.setAttribute("y2", b1y);

    liney.setAttribute("x1", b2x);
    liney.setAttribute("x2", b2x);
    liney.setAttribute("y1", b1y);
    liney.setAttribute("y2", b2y);

    b1Text.setAttribute("x", b1x);
    b1Text.setAttribute("y", b1y+10);
    b2Text.setAttribute("x", b2x);
    b2Text.setAttribute("y", b2y+10);

    let r_ = Math.sqrt((b2x-b1x)**2+(b2y-b1y)**2);
    let cosine = (b2x-b1x)/r_;
    let sine = (b2y-b1y)/r_;
    line_Text.setAttribute("x", 0);
    line_Text.setAttribute("y", 0);
    let sc = r_/90
    line_Text.style.transform = `matrix(${cosine}, ${sine}, ${-sine}, ${cosine}, ${(b1x+b2x)/2}, ${(b1y+b2y)/2}) scale(${sc, sc}) translate(-38px,-5px)`;

    textΔx.setAttribute("x", (b1x+b2x)/2);
    textΔx.setAttribute("y", b1y+15);
    textΔy.setAttribute("x", b2x+15);
    textΔy.setAttribute("y", (b1y+b2y)/2);
  };
  function checkIntersection(event){
    let x = event.offsetX;
    let y = event.offsetY;
    let b1x = b1.cx.animVal.value;
    let b1y = b1.cy.animVal.value;
    let b2x = b2.cx.animVal.value;
    let b2y = b2.cy.animVal.value;
    let b1r = b1.r.animVal.value;
    let b2r = b2.r.animVal.value;
    let sqrt = Math.sqrt
    if (sqrt((b1x-x)**2+(b1y-y)**2)<=b1r){
      selectedBall = b1;
    } else  if (sqrt((b2x-x)**2+(b2y-y)**2)<=b2r){
      selectedBall = b2;
    } else {
      selectedBall = false;
      b1.style.stroke = b2.style.stroke = "lightblue";
      return null;
    };
    line_.style.opacity = "0";
    b1.style.stroke = b2.style.stroke = "lightblue";
    selectedBall.style.stroke = "white";
    let element = document.getElementsByClassName("movableCirclesText")[0];
    console.log(element.style.opacity);
    if (element.style.opacity == "0"){
      element.style.transition = "opacity 2s";
      element.style.opacity = "1";
    };
  };
  function endMovement(){
    selectedBall = false;
    let element = document.getElementsByClassName("movableCirclesText")[0];
    if (element.style.opacity == "1"){
      element.style.transition = "opacity 2s";
      element.style.opacity = "0";
    };
    b1.style.cursor = b2.style.cursor= "grab";
    line_.style.opacity = "1";
  };

  canvas.addEventListener("mousemove", moveBall);
  canvas.addEventListener("mousedown", checkIntersection);
  canvas.addEventListener("mouseup", endMovement);
};
