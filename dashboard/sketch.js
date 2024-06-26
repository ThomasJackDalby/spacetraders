// const system_id = "X1-DF55"
const system_id = "X1-AU69"

let response_data = null;

var groupBy = function (xs, key) {
    return xs.reduce(function (rv, x) {
        (rv[x[key]] = rv[x[key]] || []).push(x);
        return rv;
    }, {});
};

async function setup() {
    createCanvas(1000, 1000);
    // const response = await fetch("https://api.spacetraders.io/v2/systems/" + system_id, {
    //     headers: {
    //         "Content-Type": "application/json",
    //         "Authorization": "Bearer "+TOKEN
    //     }
    // });
    // response_data = await response.json();
    // console.log(response_data)
}

function drawWaypoint(waypoint, x, y) {
    stroke(255);
    line(x* scale, y * scale, x * scale + 8, y * scale+12)
    line(x * scale + 8, y * scale+12, x * scale + 80, y * scale+12)

    noStroke();
    if (waypoint.type == "PLANET") {
        fill(45, 133, 76);
        ellipse(x * scale, y * scale, 20, 20);
    }
    else if (waypoint.type == "MOON") {
        fill(73, 184, 160);
        ellipse(x * scale, y * scale, 5, 5);
    }
    else if (waypoint.type == "GAS_GIANT") {
        fill(191, 115, 38);
        ellipse(x * scale, y * scale, 40, 40);
    }
    else if (waypoint.type == "ASTEROID_FIELD") {
        fill(191, 115, 38);
        ellipse(x * scale+3, y * scale-2, 3, 3);
        ellipse(x * scale-2, y * scale+3, 2, 2);
        ellipse(x * scale-2, y * scale-3, 1, 1);
        ellipse(x * scale+3, y * scale+2, 2, 2);
    }
    else if (waypoint.type == "JUMP_GATE") {
        stroke(105, 245, 245);
        strokeWeight(2);
        noFill()
        ellipse(x * scale, y * scale, 10, 10);
    }
    else {
        fill(255);
        ellipse(x * scale, y * scale, 5, 5);
    }

    fill(255);
    stroke(255);
    textSize(10);
    noStroke();
    text(waypoint.symbol, x * scale + 10, y * scale+10)
}

const scale = 5;

function draw() {
    background(0)
    // draw waypoints
    if (response_data != null) {
        noLoop();
        translate(width / 2, height / 2)
        translate(-response_data.data.x, -response_data.data.y)

        for (let i = 0; i < response_data.data.waypoints.length; i++) {
            let waypoint = response_data.data.waypoints[i];
            waypoint.location = [waypoint.x, waypoint.y];
        }

        let groups = groupBy(response_data.data.waypoints, "location");
        for (let location in groups) {
            let group = groups[location];
            drawWaypoint(group[0], group[0].x, group[0].y);
            if (group.length > 1) {
                noFill();
                stroke(200);
                strokeWeight(1);
                const radius = 40;
                ellipse(group[0].x * scale, group[0].y * scale, 2 * radius, 2 * radius);
                const delta = 2 * Math.PI / (group.length - 1);
                for (let j = 1; j < group.length; j++) {
                    let x = group[0].x + radius * Math.cos(j * delta - (Math.PI / 2)) / scale;
                    let y = group[0].y + radius * Math.sin(j * delta - (Math.PI / 2)) / scale;
                    drawWaypoint(group[j], x, y);
                }
            }
        }
    }
}