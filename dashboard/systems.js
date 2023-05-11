let systems = []

async function getData() {
    for (let j = 1; j < 200; j++) {
        url = "https://api.spacetraders.io/v2/systems/?limit=20&page="+j;
        const response = await fetch(url, {
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZGVudGlmaWVyIjoiREFMQklOR1RPTiIsImlhdCI6MTY4MzU1MjI5OCwic3ViIjoiYWdlbnQtdG9rZW4ifQ.BAn4_PBMzQCzkeeRc0hLeHBiR0xeH6YQIBB3AbKiNLD_CoX0_apyr6c_UCcyEZnTThzfDPvLr1NoenoO2Lic8LD6utploWocuQ8CnYOx7WvU_BU36G0FECxhBOcnf9wpTbCO0GBtPwVuIjor5bKQ8TKnQrjG3gSsGAYOw5N3NERzpFqRxSD_myXzoGXjkhkJ6PkqkfYyJK47-j0VHIqduU-yJsdclFhSvfHdzshYqlvc1mrhtRdy6aSlcnFJU2x71s_z16hiNZzszXmXOf7rmo3LjtTKSLo-jj86vB2Gow_ou6-UL5mbEaIl1m1iIK3Juzi0_FrJKoN1fvEzsUWMDl3z77frPzrnsJxpflNscGB2-5h1OQ1yUqjbN76uYNXri-YBOtq9XbzNabzc5O1Qn2JE09ZieVEc9BxrGjAXtkv1mSeB_BYxj_zXC2QMmBOprdGfp3ZiKd_1jWWJnuXUp7OF_8xtnKHl5IZjPHbJqtDP7zf7S-D6YqxbC0RjnXd3"
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