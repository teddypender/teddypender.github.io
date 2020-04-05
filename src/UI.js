class UI {
  constructor() {
    this.infected = null;
    this.dead = null;
    this.alive = null;
    this.recovered = null;
    this.keepDistanceCheckbox = null;
    this.dontListenGovCheckbox = null;
    this.deathRatio = null;
    this.addInfectedButton = null;
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
      this.addInfectedButton = document.querySelector('#add-infected');

      this.keepDistanceCheckbox.addEventListener('input', function () {
        GLOBAL_MULTIPLIER.separateRadius = this.checked ? 10 : 4; // simple if statement with ? :, if checked is true then radius is 10 else 4
      })
      this.deathRatio.addEventListener('mouseup', function () {
        //GLOBAL_MULTIPLIER.deathRatio = this.checked ? 0.8 : 0.2;
        if (this.value > 1) {
        GLOBAL_MULTIPLIER.deathRatio = this.value / 100;
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