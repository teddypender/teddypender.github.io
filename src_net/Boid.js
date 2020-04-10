class Boid {
  constructor(x, y, radius) {
    this.pos = new Vector(x, y);
    this.links = [];

    this.id = cuid();

    this.radius = radius || 2; //Boid size

    this.isInfected = false;
    this.isRecovered = false;
    this.health = 1;
    this.isDead = false;
    this.deathRatio = GLOBAL_MULTIPLIER.deathRatio; //0.01;
    this.infectionRatio = GLOBAL_MULTIPLIER.infectionRatio; //0.76;
    this.healingRate = GLOBAL_MULTIPLIER.healingRate; //0.76;
    this.immuneSystemStrength = Math.random(); //rand(0,1);

  }


  /**
   * @method update()
   * updates velocity, position, and acceleration
   */
  update() {
    if (this.isDead) return false;
    this.deathRatio = GLOBAL_MULTIPLIER.deathRatio;
    this.infectionRatio = GLOBAL_MULTIPLIER.infectionRatio;
    this.healingRate = GLOBAL_MULTIPLIER.healingRate;

    this.dying();
    this.healing();
  }
  
  willInfect() {
    if (random(0, 1) < this.infectionRatio) {
      return true;
    }
  }

  recover() {
    if (this.isInfected) {
      this.isInfected = false;
      this.isRecovered = true;
      this.health = 1;
      STATS.recovered[this.id] = 1;
      delete STATS.infected[this.id];
    }
  }

  dying() {
    // death ratio
    if (Math.random() < this.deathRatio) {
      if (this.isInfected) {
        this.health -= clamp(0.01, 0, 1);
      }
      if (this.health <= 0) {
        this.isDead = true;
        this.isInfected = false;
      }
    }
  }
  
  healing() {
    // healing ratio
    if (Math.random() < this.healingRate) {
      if (this.isInfected) {
        this.health += clamp(0.01, 0, 1);
        if (this.health >= 1) {
        this.isInfected = false;
        this.isRecovered = true;
        delete STATS.infected[this.id];
        }
      }
    }
  }
  

  /**
   * 
   */
  spreadInfection(boids) {
    let maxDist = Infinity;
    for (let i = 0; i < boids.length - 1; i++) {
      let boidB = boids[i];
      maxDist = dist(boidB.pos.x, boidB.pos.y, this.pos.x, this.pos.y);

      const isCloseEnough = maxDist < (this.radius + boidB.radius);
      const oneOfThemIsInfected = (this.isInfected || boidB.isInfected);
      const oneOfThemNotDead = this.isDead || boidB.isDead;
      const oneOfThemIsRecovered = this.isRecovered || boidB.isRecovered;

      if (
        isCloseEnough
        && oneOfThemIsInfected
        && !oneOfThemNotDead
        && !oneOfThemIsRecovered
        && this.willInfect()
      ) {
        if (this.isInfected) {
          boidB.isInfected = true;
          STATS.infected[boidB.id] = 1;
        }
        if (boidB.isInfected) {
          this.isInfected = true;
          STATS.infected[this.id] = 1;
        }
      }
    }
  }

  renderPaths(ctx, boids) {
  
    ctx.fillStyle =`rgb(255, 255, 255)` ;
    
    for (let i = 0; i < this.links.length - 1; i++){
      let boidB = boids[this.links[i]];
      ctx.moveTo(this.x,this.y);
      ctx.lineTo(boidB.x,boidB.y);
      ctx.stroke();
    
    }        
  }

  /**
   * Render Agent
   * @param {CanvasRenderingContext2D} ctx
   */
  render(ctx) {
    ctx.beginPath();

    ctx.save();

    ctx.fillStyle = this.isInfected ? `rgb(255, 15, 35)` : '#5bf351';
    if (this.isRecovered) ctx.fillStyle = '#395CAA';
    if (this.isDead) ctx.fillStyle = '#999999';

    ctx.translate(this.pos.x, this.pos.y);

    ctx.arc(this.radius, this.radius, this.radius, 0, 2 * Math.PI);
    ctx.stroke();
    ctx.fill();
    ctx.restore();

    ctx.closePath();
  }
}
