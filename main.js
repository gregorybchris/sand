class SandPile {
  constructor(numRows, numCols, crit) {
    this.numRows = numRows;
    this.numCols = numCols;
    this.crit = crit;

    this.sand = new Array(numRows);
    for (let r = 0; r < numRows; r++) {
      this.sand[r] = new Array(numCols);
      for (let c = 0; c < numCols; c++) {
        this.sand[r][c] = 0;
      }
    }
  }

  add(row, col, val) {
    if (row < 0 || row >= this.numRows || col < 0 || col >= this.numCols) return;
    this.sand[row][col] += val;
  }

  sub(row, col, val) {
    if (row < 0 || row >= this.numRows || col < 0 || col >= this.numCols) return;
    this.sand[row][col] -= val;
  }

  get(row, col) {
    if (row < 0 || row >= this.numRows || col < 0 || col >= this.numCols) return 0;
    return this.sand[row][col];
  }

  drop(row, col, numGrains) {
    let totalTopples = 0;
    for (let i = 0; i < numGrains; i++) {
      console.log("Adding sand...");
      this.add(row, col, 1);
      while (true) {
        // console.log("Updating...");
        const numTopples = this.update(this.sand, row, col, this.crit);
        if (numTopples == 0) break;
        console.log(`Updated with ${numTopples} topples`);
        totalTopples += numTopples;
      }
    }

    return totalTopples;
  }

  getTopples() {
    const topples = [];
    for (let row = 0; row < this.sand.length; row++) {
      for (let col = 0; col < this.sand[0].length; col++) {
        if (this.get(row, col) > this.crit) {
          const topple = { row: row, col: col };
          topples.push(topple);
        }
      }
    }
    return topples;
  }

  update() {
    const topples = this.getTopples();
    topples.forEach((topple) => {
      const { row, col } = topple;
      this.sub(row, col, 4);
      for (let r = -1; r <= 1; r++) {
        for (let c = -1; c <= 1; c++) {
          if (r * c == 0 && r + c != 0) {
            this.add(row + r, col + c, 1);
          }
        }
      }
    });
    return topples.length;
  }
}

const center = (numRows, numCols) => {
  const row = Math.round(numRows / 2);
  const col = Math.round(numCols / 2);
  return { row: row, col: col };
};

const numRows = 6;
const numCols = 5;
const critical = 4;
const numDrops = 100;

const pile = new SandPile(numRows, numCols, critical);
console.log(pile.sand);
const { row, col } = center(numRows, numCols);
const numTopples = pile.drop(row, col, numDrops);
console.log(pile.sand);
console.log("Num topples: ", numTopples);

const canvas = document.querySelector("canvas");
// canvas.attr("width", "300").attr("height", "300");

const context = canvas.getContext("2d");

const draw = (pile, context) => {
  const width = 40;
  const height = 40;
  context.fillStyle = "rgb(26, 102, 133)";
  context.strokeStyle = "rgb(13, 66, 87)";
  for (let row = 0; row < pile.numRows; row++) {
    for (let col = 0; col < pile.numCols; col++) {
      const size = pile.get(row, col);
      context.fillRect(0 + col * width, 0 + row * height, width, height);
      context.strokeRect(0 + col * width, 0 + row * height, width, height);
    }
  }
};

draw(pile, context);
