class Boid {
  constructor(x, y, radius) {
    this.pos = new Vector(x, y);
    this.acc = new Vector(0, 0);
    this.vel = new Vector.random2D(0, 0);
    this.vel.mult(10);

    this.id = cuid();

    this.radius = radius || 1; //Boid size
    this.maxSpeed = 1.0;
    this.maxForce = 0.05;
    this.mass = 0.5;

    // this.isInfected = randomInt(2) < 0.5 ? true : false;
    this.isInfected = false;
    this.isRecovered = false;
    this.health = 1;
    this.isDead = false;
    this.deathRatio = GLOBAL_MULTIPLIER.deathRatio; //0.01;
    this.infectionRatio = GLOBAL_MULTIPLIER.infectionRatio; //0.76;
    this.healingRate = GLOBAL_MULTIPLIER.healingRate; //0.76;
    this.immuneSystemStrength = Math.random(); //rand(0,1);

    this.flock = new Flock(this);
    this.flockMultiplier = GLOBAL_MULTIPLIER;
  }


  /**
   * @method update()
   * updates velocity, position, and acceleration
   */
  update() {
    if (this.isDead) return false;
    this.vel.add(this.acc);
    this.vel.limit(this.maxSpeed);
    this.pos.add(this.vel);
    this.deathRatio = GLOBAL_MULTIPLIER.deathRatio;
    this.infectionRatio = GLOBAL_MULTIPLIER.infectionRatio;
    this.healingRate = GLOBAL_MULTIPLIER.healingRate;

    this.acc.mult(0);

    this.dying();
    this.healing();
  }

  setMaxSpeed(max) {
    this.maxSpeed = max;
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

  visitHospital(hospitals) {
    let record = Infinity;
    let close = null;

    for (let i = hospitals.length - 1; i >= 0; i--) {
      let hospital = hospitals[i];
      if (!this.isInfected) {
        this.applyForce(this.flock.flee(hospital.pos).mult(5));
        continue;
      }
      const maxDist = dist(this.pos.x, this.pos.y, hospital.pos.x, hospital.pos.y);

      const isCloseEnough = (maxDist < this.radius + 5);
      const shouldVisit = maxDist < record && maxDist && !hospitals[i].isFull();

      if (isCloseEnough) {
        hospitals[i].heal(this);
      } else if (shouldVisit) {
        record = maxDist;
        close = hospital.pos;
      }
    }
    // seek
    if (close !== null) {
      return this.applyForce(this.flock.seek(close).mult(0.8));
    }
    return this.applyForce(new Vector(0, 0))
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
   * @method applyForce()
   * @param {Vector} f 
   * applies force to acceleration
   */
  applyForce(f) { this.acc.add(f) }


  /**
   * @method boundaries()
   * check boundaries and limit agents within screen
   */
  boundaries() {
    let d = 10;
    let desire = null;
    if (this.pos.x < d) {
      desire = new Vector(this.maxSpeed, this.vel.y);
    } else if (width < this.pos.x) {
      desire = new Vector(-this.maxSpeed, this.vel.y);
    }
    if (this.pos.y < 0) {
      desire = new Vector(this.vel.y, this.maxSpeed);
    } else if (this.pos.y > height - (this.radius * 2)) {
      desire = new Vector(this.vel.x, -this.maxSpeed);
    }

    if (desire) {
      desire.normalize();
      desire.mult(this.maxSpeed);
      let steer = Vector.sub(desire, this.vel);
      this.applyForce(steer);
    }
  }


  /**
   * @method applyFlock()
   * @param {*} agents 
   * calculates all the flocking code apply it to the acceleration
   */
  applyFlock(agents) {
    let sep = this.flock.separate(agents);
    let ali = this.flock.align(agents);
    let coh = this.flock.cohesion(agents);
    let wander = this.flock.wander();

    sep.mult(this.flockMultiplier.separate);
    ali.mult(this.flockMultiplier.align);
    coh.mult(this.flockMultiplier.cohesion);
    wander.mult(this.flockMultiplier.wander);

    this.applyForce(sep);
    this.applyForce(ali);
    this.applyForce(coh);
    this.applyForce(wander);
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
  
  healNaturally(boid) {
    if (boid.isInfected && 0.7 < this.immuneSystemStrength) {
      boid.recover();
      boid.isRecovered = true;
      //this.healed[boid.id] = 1;
    } 
  }


  /**
   * Render Agent
   * @param {CanvasRenderingContext2D} ctx
   */
  render(ctx) {
    ctx.beginPath();
    let angle = this.vel.heading();

    ctx.save();

    ctx.fillStyle = this.isInfected ? `rgb(255, 15, 35)` : '#5bf351';
    if (this.isRecovered) ctx.fillStyle = '#395CAA';
    if (this.isDead) ctx.fillStyle = '#999999';

    ctx.translate(this.pos.x, this.pos.y);
    ctx.rotate(angle);
    ctx.moveTo(this.radius, 0);
    ctx.lineTo(-this.radius, -this.radius + 1);
    ctx.lineTo(-this.radius, this.radius - 2);
    ctx.lineTo(this.radius, 0);
    ctx.fill();
    ctx.restore();

    ctx.closePath();
  }
}
