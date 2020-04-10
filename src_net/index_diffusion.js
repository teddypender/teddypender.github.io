

let width = window.innerWidth;
let height = window.innerHeight;

const FLEE_RADIUS = 10;
const BOIDS_COUNT = 1000;
const IMMUNE_COUNT = 200;
const INFECTED_COUNT = 100;
const GLOBAL_MULTIPLIER = {
  infectionRatio: 0.65,
  healingRate: 0.05,
  deathRatio: 0.2,
  maxDistForLinks: 100
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

  for (let i = 0; i < BOIDS_COUNT; i++) {
    boids.push(new Boid(random(width), random(height)))
  }
  
  for (let i = 0; i < INFECTED_COUNT; i++) {
    boids[i].isInfected = true;
  }
  
  for (let i = INFECTED_COUNT; i < INFECTED_COUNT + IMMUNE_COUNT; i++) {
    boids[i].isRecovered = true;
  }
  
 
  for (let i = 0; i < boids.length - 1; i++){
    let boidA = boids[i];
    for (let j = 0; j < boids.length - 1; j++){
      if (i != j) {
        let boidB = boids[j];
        boidDist = dist(boidB.pos.x, boidB.pos.y, boidA.pos.x, boidA.pos.y);
        const linkOrNah = boidDist < GLOBAL_MULTIPLIER.maxDistForLinks;
        if (linkOrNah) {
          boidA.links.push(j); 
        }
      }
    }
  }


  function animate() {
  
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, width, height);

    for (let i = boids.length - 1; i >= 0; i--) {
      const boid = boids[i];
      boid.update()
      boid.spreadInfection(boids);

      boid.render(ctx);
      boid.renderPaths(ctx, boids);

      if (boid.isDead) STATS.dead[boid.id] = 1;
      if (boid.isInfected) STATS.infected[boid.id] = 1;
      if (boid.isRecovered) STATS.recovered[boid.id] = 1;
    }

    ui.printStats(boids.length);

    requestAnimationFrame(animate);
  }
  animate();

}