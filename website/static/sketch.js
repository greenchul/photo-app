console.log("connected")

let cam
let canvas
let img
let camera

function preload(){
    // camera
   img = loadImage("static/sketch/slr_cam.jpg")
   camera = loadModel("static/sketch/slr_cam.obj")
}  

function setup() {
    canvas =  createCanvas(600, 600, WEBGL);
     
    
      
    cam = createCamera()
    cam.setPosition(0,-150,350)
    cam.lookAt(0,0,0)
     
     
     
   }

   function draw(){
       background(255)
       lights()
    translate(0,0,0)

    push()
    translate(0,0,0)
    texture(img);
    model(camera)
    noStroke()
    pop()

   }