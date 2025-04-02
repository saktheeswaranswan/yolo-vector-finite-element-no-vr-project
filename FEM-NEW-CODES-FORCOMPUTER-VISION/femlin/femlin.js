let nElementsInput, barLengthInput, solveButton, exportElemButton, exportGlobalButton, exportAllButton, exportMassButton;
let elementInputs = [];
let nElements, barLength;
let nodes = [], individualStiffness = [], globalStiffness = [], fullForce = [], displacements = [], massMatrix = [];
let canvas;

function setup() {
    canvas = createCanvas(600, 600);
    canvas.position(10, 150);
    
    createP("Number of Elements:").position(10, 10);
    nElementsInput = createInput("3").position(10, 40);
    
    createP("Total Bar Length:").position(200, 10);
    barLengthInput = createInput("1000").position(200, 40);
    
    let createInputsButton = createButton("Create Element Inputs").position(400, 40);
    createInputsButton.mousePressed(createInputFields);
    
    solveButton = createButton("Solve FEM").position(10, 80).hide();
    solveButton.mousePressed(solveFEM);
    
    exportElemButton = createButton("Export Element Stiffness CSV").position(620, 200).hide();
    exportElemButton.mousePressed(exportElementCSV);
    
    exportGlobalButton = createButton("Export Global Stiffness CSV").position(620, 240).hide();
    exportGlobalButton.mousePressed(exportGlobalCSV);
    
    exportAllButton = createButton("Export All Results CSV").position(620, 280).hide();
    exportAllButton.mousePressed(exportAllCSV);
    
    exportMassButton = createButton("Export Mass Matrix CSV").position(620, 320).hide();
    exportMassButton.mousePressed(exportMassCSV);
}

function createInputFields() {
    nElements = int(nElementsInput.value());
    barLength = parseFloat(barLengthInput.value());
    if (isNaN(nElements) || nElements < 1 || isNaN(barLength) || barLength <= 0) {
        alert("Enter valid values for elements and bar length.");
        return;
    }
    elementInputs = [];
    clearCanvas();
    
    for (let i = 0; i < nElements; i++) {
        let yPos = 120 + i * 30;
        createP(`Element ${i + 1} E:`).position(10, yPos);
        let inpE = createInput("200000").position(50, yPos);
        createP("A:").position(200, yPos);
        let inpA = createInput("25").position(230, yPos);
        createP("Load:").position(370, yPos);
        let inpLoad = createInput("1000").position(420, yPos);
        elementInputs.push([inpE, inpA, inpLoad]);
    }
    solveButton.show();
    exportElemButton.hide();
    exportGlobalButton.hide();
    exportAllButton.hide();
    exportMassButton.hide();
}

function clearCanvas() {
    background(255);
}

function solveFEM() {
    clearCanvas();
    let nNodes = nElements + 1;
    nodes = Array.from({ length: nNodes }, (_, i) => (i * barLength) / nElements);
    individualStiffness = [];
    globalStiffness = Array(nNodes).fill().map(() => Array(nNodes).fill(0));
    fullForce = Array(nNodes).fill(0);
    massMatrix = Array(nNodes).fill().map(() => Array(nNodes).fill(0));
    
    for (let i = 0; i < nElements; i++) {
        let [inpE, inpA, inpLoad] = elementInputs[i];
        let E = parseFloat(inpE.value());
        let A = parseFloat(inpA.value());
        let elemLoad = parseFloat(inpLoad.value());
        
        let L = nodes[i + 1] - nodes[i];
        let k = (E * A) / L;
        let kMatrix = [
            [k, -k],
            [-k, k]
        ];
        individualStiffness.push(kMatrix);
        
        globalStiffness[i][i] += k;
        globalStiffness[i][i + 1] -= k;
        globalStiffness[i + 1][i] -= k;
        globalStiffness[i + 1][i + 1] += k;
        
        fullForce[i] += elemLoad / 2;
        fullForce[i + 1] += elemLoad / 2;
        
        let m = (A * L) / 6;
        let mMatrix = [
            [2 * m, m],
            [m, 2 * m]
        ];
        massMatrix[i][i] += mMatrix[0][0];
        massMatrix[i][i + 1] += mMatrix[0][1];
        massMatrix[i + 1][i] += mMatrix[1][0];
        massMatrix[i + 1][i + 1] += mMatrix[1][1];
    }
    
    displacements = numeric.solve(globalStiffness, fullForce);
    displayResults();
    exportElemButton.show();
    exportGlobalButton.show();
    exportAllButton.show();
    exportMassButton.show();
}

function displayResults() {
    clearCanvas();
    textSize(14);
    fill(0);
    text("Global Stiffness Matrix:", 10, 20);
    for (let i = 0; i < globalStiffness.length; i++) {
        text(globalStiffness[i].join(", "), 10, 40 + i * 20);
    }
    text("Displacements:", 10, 60 + globalStiffness.length * 20);
    text(displacements.join(", "), 10, 80 + globalStiffness.length * 20);
}

function exportMassCSV() {
    let csvContent = "Mass Matrix\n";
    csvContent += massMatrix.map(row => row.join(",")).join("\n") + "\n\n";
    saveStrings(csvContent.split("\n"), "mass_matrix.csv");
}
