let scaleF = 1;
let offset;

async function getData() {
    let limit = 20;
    let total = 5000;
    for (let j = 1; j < (total / limit) + 1; j++) {
        url = "https://api.spacetraders.io/v2/systems/?limit=20&page=" + j;
        const response = await fetch(url, {
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + TOKEN
            }
        });
        let responseData = await response.json();
        console.log(responseData);
        for (let i = 0; i < responseData.data.length; i++) {
            systems.push(responseData.data[i]);
        }
        await sleep(500);
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function setup() {
    createCanvas(windowWidth, windowHeight);
    // await getData();

    offset = createVector(0, 0);

    window.addEventListener("wheel", e => {
        const scaleDelta = 1 - (e.deltaY / 1000);
        scaleF *= scaleDelta;
        console.log(scaleF);
        const mouse = createVector(mouseX, mouseY);
        offset.sub(mouse).mult(scaleDelta).add(mouse)
    });
}

function scaledCircle(x, y, r) {
    ellipse(x * scaleF, y * scaleF, r * scaleF, r * scaleF);
}
function scaledLine(x1, y1, x2, y2) {
    line(x1 * scaleF, y1 * scaleF, x2 * scaleF, y2 * scaleF);
}

function drawLabel(label, x, y) {
    line(x * scaleF, y * scaleF, x * scaleF + 8, y * scaleF + 12)
    line(x * scaleF + 8, y * scaleF + 12, x * scaleF + 80, y * scaleF + 12)
    text(label, x * scaleF + 10, y * scaleF + 10)
}

function drawWaypoint(waypoint, x, y, drawLabels) {
    const waypointScale = 0.02;

    if (drawLabels) {
        stroke(255);
        line(x * scaleF, y * scaleF, x * scaleF + 8, y * scaleF + 12)
        line(x * scaleF + 8, y * scaleF + 12, x * scaleF + 80, y * scaleF + 12)
    }
    noStroke();
    if (waypoint.type == "PLANET") {
        fill(45, 133, 76);
        scaledCircle(x, y, 20*waypointScale);
    }
    else if (waypoint.type == "MOON") {
        fill(73, 184, 160);
        scaledCircle(x, y, 5*waypointScale);
    }
    else if (waypoint.type == "GAS_GIANT") {
        fill(191, 115, 38);
        scaledCircle(x, y, 40*waypointScale);
    }
    else if (waypoint.type == "ASTEROID_FIELD") {
        fill(191, 115, 38);
        // ellipse(x * scaleF+3, y * scaleF-2, 3, 3);
        // ellipse(x * scaleF-2, y * scaleF+3, 2, 2);
        // ellipse(x * scaleF-2, y * scaleF-3, 1, 1);
        // ellipse(x * scaleF+3, y * scaleF+2, 2, 2);
    }
    else if (waypoint.type == "JUMP_GATE") {
        stroke(105, 245, 245);
        strokeWeight(2);
        noFill()
        scaledCircle(x, y, 10*waypointScale);
    }
    else {
        fill(255);
        scaledCircle(x, y, 5*waypointScale);
    }
    if (drawLabels) {
        fill(255);
        stroke(255);
        textSize(20);
        noStroke();
        text(waypoint.symbol, x * scaleF + 10, y * scaleF + 10)
    }
}

const majorGridSpacing = 100;
const minorGridSpacing = 10;

function drawVerticalLines(x1, y1, x2, y2, spacing) {
    let x = Math.floor(x1 / spacing) * spacing;
    while (x < x2 - spacing) {
        x += spacing;
        scaledLine(x, y1, x, y2);
        push()
        fill(255);
        noStroke();
        text(x, x * scaleF, y1 * scaleF-4);
        pop();
    }
}
function drawHorizontalLines(x1, y1, x2, y2, spacing) {
    let y = Math.floor(y1 / spacing) * spacing;
    while (y < y2 - spacing) {
        y += spacing;
        scaledLine(x1, y, x2, y);
        push()
        fill(255);
        noStroke();
        translate(x1 * scaleF, y * scaleF);
        rotate(radians(-90));
        text(y, 0, -4);
        pop();
    }
}

const noDrawMargin = 20;

function draw() {
    background(0)
    translate(offset.x, offset.y);

    let left = (-offset.x + noDrawMargin) / scaleF;
    let bottom = (-offset.y + noDrawMargin) / scaleF;
    let width = (windowWidth - 2*noDrawMargin) / scaleF;
    let height = (windowHeight - 2*noDrawMargin) / scaleF;

    noStroke()
    fill(255)
    textSize(20)
    text(scaleF.toFixed(3), left * scaleF, (bottom + height) * scaleF+18)

    strokeWeight(2);
    stroke(52)
    noFill();
    rect(left * scaleF, bottom * scaleF, width * scaleF, height * scaleF)

    // draw grid lines
    if (scaleF > 0.5) {
        textSize(20)
        strokeWeight(3);
        drawVerticalLines(left, bottom, left + width, bottom + height, majorGridSpacing)
        drawHorizontalLines(left, bottom, left + width, bottom + height, majorGridSpacing)
    }
    if (scaleF > 5) {
        textSize(15)
        strokeWeight(1)
        drawVerticalLines(left, bottom, left + width, bottom + height, minorGridSpacing)
        drawHorizontalLines(left, bottom, left + width, bottom + height, minorGridSpacing)
    }

    for (let k = 0; k < systems.length; k++) {
        let system = systems[k];
        
        if (system.x < left || system.x > left + width) continue;
        if (system.y < bottom || system.y > bottom + height) continue;

        if (scaleF > 2) {
            noStroke();
            fill(255);
            textSize(20);
            drawLabel(system.symbol, system.x, system.y);
        }

        noStroke()
        fill(255);
        if (system.type == "RED_STAR") fill(201, 67, 34);
        else if (system.type == "ORANGE_STAR") fill(201, 137, 34);
        else if (system.type == "BLUE_STAR") fill(81, 169, 207);
        else if (system.type == "YOUNG_STAR") fill(226, 247, 106);

        let scaleW = 0.1

        if (scaleF >= 2.5) {
            scaledCircle(system.x, system.y, 1.25);
            for (let j = 0; j < system.waypoints.length; j++) {
                let waypoint = system.waypoints[j];
                let drawLabels = scaleF > 20;
                stroke(255)
                strokeWeight(1);
                line(system.x * scaleF, system.y * scaleF, (system.x + waypoint.x * scaleW) * scaleF, (system.y + waypoint.y * scaleW) * scaleF)
                drawWaypoint(waypoint, system.x + waypoint.x * scaleW, system.y + waypoint.y * scaleW, drawLabels);
            }
        }

        ellipse(system.x * scaleF, system.y * scaleF, 10, 10);
    }

    if (mouseIsPressed) {
        offset.x -= pmouseX - mouseX;
        offset.y -= pmouseY - mouseY;
    }
}