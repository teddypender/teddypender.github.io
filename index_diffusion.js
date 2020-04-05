

let width = window.innerWidth;
let height = window.innerHeight;

const FLEE_RADIUS = 100;
const BOIDS_COUNT = 5000;
const IMMUNE_COUNT = 0;
const INFECTED_COUNT = 100;
const HOSPITALS_COUNT = 0;
const HOSPITAL_MAX_CAPACITY = 10;
const GLOBAL_MULTIPLIER = {
  separateRadius: 4,
  separate: 1.2,
  align: 0.8,
  cohesion: 0.3,
  wander: 0.5,
  maxSpeed: 1.0
  //deathRatio: 0.0
}
// map of boid ids
const STATS = {
  dead: {},
  infected: {},
  recovered: {}
}

const ui = new UI();
ui.init();

window.onload = function () {
  // stats 
  const canvas = document.getElementById('c');
  const ctx = canvas.getContext('2d');
  width = canvas.width = window.innerWidth;
  height = canvas.height = window.innerHeight;

  const boids = [];
  const hospitals = [];
  const addInfectedBoid = () => {
    let infectedBoid = new Boid(random(width), random(height));
    infectedBoid.isInfected = true;
    boids.push(infectedBoid);
  }

  for (let i = 0; i < BOIDS_COUNT; i++) {
    boids.push(new Boid(random(width), random(height)))
  }

  for (let i = 0; i < HOSPITALS_COUNT; i++) {
    hospitals.push(new Hospital(random(width), random(height)))
  }
  
  for (let i = 0; i < INFECTED_COUNT; i++) {
    boids[i].isInfected = true
  }
  
  for (let i = INFECTED_COUNT; i < INFECTED_COUNT + IMMUNE_COUNT; i++) {
    boids[i].isRecovered = true
  }


  // click to place hospitals
  //canvas.addEventListener('click', (e) => {
  //  hospitals.push(new Hospital(e.offsetX, e.offsetY))
  //})
  ui.addInfectedButton.addEventListener('click', function () {
    addInfectedBoid();
    addInfectedBoid();
  })

  function animate() {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, width, height);

    for (let i = boids.length - 1; i >= 0; i--) {
      const boid = boids[i];
      boid.update()
      boid.applyFlock(boids);
      boid.boundaries();
      boid.spreadInfection(boids);
      boid.healNaturally(boid);

      boid.visitHospital(hospitals)
      boid.setMaxSpeed(GLOBAL_MULTIPLIER.maxSpeed)
      boid.render(ctx);

      if (boid.isDead) STATS.dead[boid.id] = 1;
    }

    hospitals.forEach(h => h.render(ctx))

    ui.printStats(boids.length);

    requestAnimationFrame(animate);
  }
  animate();

}