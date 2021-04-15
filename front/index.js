window.addEventListener('load', async function () {
    class MlbData {
        constructor(url) {
            this.url = url;
            this._data = null;
        }
        async getPlayerList() {
            let a = await fetch(this.url);       // The Promise returned from fetch()
            let data = await a.text();
            data = JSON.parse(data);
            this._data = data;
            return data;
        }
        static valuedFormat(inputValue) {
            inputValue = inputValue.toLowerCase();
            inputValue = inputValue.replace(" ", "");
            return inputValue;
        }
        getID(playerName) {
            if (playerName === "") {
                return -3;
            }
            let _id;
            for (let i = 0; i < this._data.length; i++) {
                if (MlbData.valuedFormat(this._data[i]["name"]) === playerName) {
                    _id = this._data[i]["id"]
                    return _id;
                }
                else {
                    return -1;
                }
            }
        }
        async fromDataBase(newURL) {
            let aa = await fetch(newURL);

            let player = await aa.text();
            player = JSON.parse(player);
            return player;
        }
    };

    let mlbdata;
    let input_ = document.querySelector('.enterButton');
    input_.addEventListener('click', async function () {
        if (false && mlbdata === undefined) {
            mlbdata = new MlbData('https://minchulcho.github.io/staticResoure/list.json');
            await mlbdata.getPlayerList();
        }

        let inputSelector = document.querySelector('input');
        /*
            connect with server
        */
        let res = await fetch('http://13.52.181.55:3000/name2id?name='+encodeURIComponent(inputSelector.value));
        res = await res.json()
        
        // JSON.parse(await res.text())
        // let pName = MlbData.valuedFormat(inputSelector.value);


        let pID = res.id;//mlbdata.getID(pName);
        let checkTalbe = document.querySelector("#playerTable")
        // if ( checkTalbe  ){
        //     checkTalbe.remove();
        // }
        checkTalbe && checkTalbe.remove();
        // console.log(pID);

        //pID = 425783
        if (pID > 0) {
            let url = ('https://statsapi.mlb.com/api/v1/people/' + pID + '?hydrate=currentTeam,team,stats(type=[yearByYear,yearByYearAdvanced,careerRegularSeason,careerAdvanced,availableStats](team(league)),leagueListId=mlb_hist)&site=en');
            let urlx = 'https://minchulcho.github.io/staticResoure/' + (pID).toString() + '.json';
            // let aa = await mlbdata.fromDataBase(url);
            let aa = await fetch(url);
            aa = await aa.json()

            let info = aa["people"][0]
            if (info["stats"][0]["group"]["displayName"] === "hitting") {
                console.log(info["fullName"] + "is a hitter")
            }

            let yearByyear = aa["people"][0]["stats"][0]["splits"]
            //console.log ( yearByyear)

            let table_ = document.createElement("table");
            table_.setAttribute("class", "playerTableCSS")
            table_.setAttribute("id", "playerTable");
            document.querySelector("#info").appendChild(table_)
            console.log("year\tavg\t\tHR\t")
            let tr1 = document.createElement("tr");
            table_.appendChild(tr1);
            let th1_1 = document.createElement("th");
            tr1.appendChild(th1_1);

            let th1_2 = document.createElement("th");
            tr1.appendChild(th1_2);

            let th1_3 = document.createElement("th");
            tr1.appendChild(th1_3);

            th1_1.innerText = "year";
            th1_2.innerText = "avg";
            th1_3.innerText = "HR";





            for (let i = 0; i < yearByyear.length; i++) {
                let tr2 = document.createElement("tr");
                table_.appendChild(tr2);

                let th2_1 = document.createElement("td");
                tr2.appendChild(th2_1);

                let th2_2 = document.createElement("td");
                tr2.appendChild(th2_2);

                let th2_3 = document.createElement("td");
                tr2.appendChild(th2_3);


                th2_1.innerText = yearByyear[i]["season"];
                th2_2.innerText = yearByyear[i]["stat"]["avg"];
                th2_3.innerText = yearByyear[i]["stat"]["homeRuns"];
            }

        }
        else {
            // alert("Line74 : not valued input ");
        }
    });





});