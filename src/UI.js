class UI {
  constructor() {
    this.infected = null;
    this.dead = null;
    this.alive = null;
    this.recovered = null;
    this.keepDistanceCheckbox = null;
    this.dontListenGovCheckbox = null;
    this.deathRatio = null;
    //this.addInfectedButton = null;
    this.infectionRatio = null;
    this.healingRate = null;
  }

  init() {
    window.addEventListener('load', () => {
      this.infected = document.querySelector('#infected');
      this.dead = document.querySelector('#dead');
      this.alive = document.querySelector('#alive');
      this.recovered = document.querySelector('#recovered');
      this.keepDistanceCheckbox = document.querySelector('#keep-distance');
      this.dontListenGovCheckbox = document.querySelector('#dont-listen');
      this.deathRatio = document.querySelector('#deadliness');
      this.infectionRatio = document.querySelector('#transmissibility');
      this.healingRate = document.querySelector('#healing');
      //this.addInfectedButton = document.querySelector('#add-infected');

      this.keepDistanceCheckbox.addEventListener('input', function () {
        GLOBAL_MULTIPLIER.separateRadius = this.checked ? 10 : 4; // simple if statement with ? :, if checked is true then radius is 10 else 4
      })
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
      this.dontListenGovCheckbox.addEventListener('input', function () {
        GLOBAL_MULTIPLIER.separateRadius = this.checked ? 2 : 4;
        GLOBAL_MULTIPLIER.maxSpeed = this.checked ? 5 : 1.8;
      })
      
      var slider = document.getElementById("deadliness");
      var output = document.getElementById("demo");
      output.innerHTML = slider.value; // Display the default slider value
        
        // Update the current slider value (each time you drag the slider handle)
      slider.oninput = function() {
          output.innerHTML = this.value / 100;
        }
      var slider_trans = document.getElementById("transmissibility");
      var output_trans = document.getElementById("demo_trans");
      output_trans.innerHTML = slider_trans.value; // Display the default slider value
        
        // Update the current slider value (each time you drag the slider handle)
      slider_trans.oninput = function() {
          output_trans.innerHTML = this.value / 100;
        }
        
      var slider_heal = document.getElementById("healing");
      var output_heal = document.getElementById("demo_heal");
      output_heal.innerHTML = slider_trans.value; // Display the default slider value
        
        // Update the current slider value (each time you drag the slider handle)
      slider_heal.oninput = function() {
          output_heal.innerHTML = this.value / 100;
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