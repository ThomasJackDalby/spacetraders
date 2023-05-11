let systems = []

async function getData() {
    for (let j = 1; j < 200; j++) {
        url = "https://api.spacetraders.io/v2/systems/?limit=20&page="+j;
        const response = await fetch(url, {
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer "+TOKEN
            }
        });
        console.log(response.statusText);
        let responseData = await response.json();
        for (let i = 0; i < responseData.data.length; i++) {
            let system = responseData.data[i];
            systems.push(createVector(system.x, system.y));
        }
        await sleep(550);
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function setup() {
    createCanvas(2000, 1000);
    await getData();
}

function draw() {
    background(0)
    translate(width/2, height/2)

    fill(255, 0, 0);
    for (let k = 0; k < systems.length; k++) {
        let system = systems[k];
        ellipse(system.x*0.05, system.y*0.05, 5, 5);
    }
}