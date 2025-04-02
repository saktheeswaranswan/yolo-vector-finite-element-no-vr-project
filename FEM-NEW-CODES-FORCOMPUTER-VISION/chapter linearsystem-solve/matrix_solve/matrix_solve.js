let nInput, createMatrixButton, solveButton;
let matrixInputs = [];
let vectorInputs = [];
let n;
let solutionP;

function setup() {
  noCanvas();
  // Input for matrix dimension
  createP("Enter matrix dimension (n):");
  nInput = createInput('');
  createMatrixButton = createButton("Create Matrix");
  createMatrixButton.mousePressed(createMatrixInputs);
  
  // Button to solve the system (hidden until matrix inputs are created)
  solveButton = createButton("Solve");
  solveButton.mousePressed(solveGaussian);
  solveButton.hide();
  
  solutionP = createP("");
}

function createMatrixInputs() {
  // Remove any previous inputs
  matrixInputs.forEach(row => row.forEach(input => input.remove()));
  vectorInputs.forEach(input => input.remove());
  matrixInputs = [];
  vectorInputs = [];
  
  n = int(nInput.value());
  if (isNaN(n) || n < 1) {
    alert("Please enter a valid positive integer for n");
    return;
  }
  
  // Create inputs for matrix A
  createP("Enter matrix A entries:");
  for (let i = 0; i < n; i++) {
    let rowInputs = [];
    let rowDiv = createDiv();
    for (let j = 0; j < n; j++) {
      let inp = createInput('');
      inp.size(50);
      rowInputs.push(inp);
    }
    matrixInputs.push(rowInputs);
  }
  
  // Create inputs for vector B
  createP("Enter vector B entries:");
  for (let i = 0; i < n; i++) {
    let inp = createInput('');
    inp.size(50);
    vectorInputs.push(inp);
  }
  
  solveButton.show();
}

function solveGaussian() {
  // Read inputs into arrays A and B
  let A = [];
  let B = [];
  for (let i = 0; i < n; i++) {
    A[i] = [];
    for (let j = 0; j < n; j++) {
      A[i][j] = parseFloat(matrixInputs[i][j].value());
      if (isNaN(A[i][j])) {
        alert("Please enter valid numbers for matrix A.");
        return;
      }
    }
  }
  for (let i = 0; i < n; i++) {
    B[i] = parseFloat(vectorInputs[i].value());
    if (isNaN(B[i])) {
      alert("Please enter valid numbers for vector B.");
      return;
    }
  }
  
  // Solve the system using Gaussian elimination
  let solution = gaussianElimination(A, B);
  displaySolution(solution);
}

function gaussianElimination(A, B) {
  let N = n;
  // Forward elimination
  for (let k = 0; k < N - 1; k++) {
    // Loop over rows below pivot
    for (let i = k + 1; i < N; i++) {
      let factor = A[i][k] / A[k][k];
      for (let j = k + 1; j < N; j++) {
        A[i][j] = A[i][j] - factor * A[k][j];
      }
      B[i] = B[i] - factor * B[k];
    }
  }
  
  // Back substitution
  let X = new Array(N);
  X[N - 1] = B[N - 1] / A[N - 1][N - 1];
  for (let i = N - 2; i >= 0; i--) {
    let sum = 0;
    for (let j = i + 1; j < N; j++) {
      sum += A[i][j] * X[j];
    }
    X[i] = (B[i] - sum) / A[i][i];
  }
  return X;
}

function displaySolution(solution) {
  let output = "<strong>Solution:</strong><br>";
  for (let i = 0; i < solution.length; i++) {
    output += "x" + (i + 1) + " = " + solution[i] + "<br>";
  }
  solutionP.html(output);
}
