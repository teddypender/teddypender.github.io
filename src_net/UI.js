class UI {
  constructor() {
    this.infected = null;
    this.dead = null;
    this.alive = null;
    this.recovered = null;
    this.deathRatio = 0.35;
    this.infectionRatio = 0.65;
    this.healingRate = 0.05;
  }

  init() {
    window.addEventListener('load', () => {
      this.infected = document.querySelector('#infected');
      this.dead = document.querySelector('#dead');
      this.alive = document.querySelector('#alive');
      this.recovered = document.querySelector('#recovered');
      this.deathRatio = document.querySelector('#deadliness');
      this.infectionRatio = document.querySelector('#transmissibility');
      this.healingRate = document.querySelector('#healing');

      this.deathRatio.addEventListener('mouseup', function () {
        if (this.value > -1) {
        GLOBAL_MULTIPLIER.deathRatio = this.value / 100;
        }
      })
      
      this.healingRate.addEventListener('mouseup', function () {
        if (this.value > -1) {
        GLOBAL_MULTIPLIER.healingRate = this.value / 100;
        }
      })
      
      this.infectionRatio.addEventListener('mouseup', function () {
        if (this.value > -1) {
        GLOBAL_MULTIPLIER.infectionRatio = this.value / 100;
        }
      })

      var slider = document.getElementById("deadliness");
      var output = document.getElementById("demo");
      output.innerHTML = slider.value; // Display the default slider value
        
        // Update the current slider value (each time you drag the slider handle)
      slider.oninput = function() {
          output.innerHTML = this.value;
        }
        
      var slider_trans = document.getElementById("transmissibility");
      var output_trans = document.getElementById("demo_trans");
      output_trans.innerHTML = slider_trans.value; // Display the default slider value
        
        // Update the current slider value (each time you drag the slider handle)
      slider_trans.oninput = function() {
          output_trans.innerHTML = this.value;
        }
        
      var slider_heal = document.getElementById("healing");
      var output_heal = document.getElementById("demo_heal");
      output_heal.innerHTML = slider_heal.value; // Display the default slider value
        
        // Update the current slider value (each time you drag the slider handle)
      slider_heal.oninput = function() {
          output_heal.innerHTML = this.value;
        }
    })
  }

  printStats(boidsCount) {
    const deadCount = Object.values(STATS.dead).length;
    const infectedCount = Object.values(STATS.infected).length;
    const recoveredCount = Object.values(STATS.recovered).length;
    const aliveCount = boidsCount - deadCount - infectedCount - recoveredCount;


    this.alive.innerText = Math.max(0, aliveCount);
    this.dead.innerText = Math.max(0, deadCount);
    this.infected.innerText = Math.max(0, infectedCount - deadCount)
    this.recovered.innerText = Math.max(0, recoveredCount)
  }
}