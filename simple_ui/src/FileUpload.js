import React, { useEffect, useState } from 'react';
import ReportLesson from './ReportLesson';
import classes from './FileUpload.module.css'

const URL = "ws:localhost:5003/ws";

function FileUpload(){
    const [chosenFile, setChosenFile] = useState(null);
    const [data, setData] = useState(null);
    const [ws, setWs] = useState(null);

    useEffect(() => {
        setWs(new WebSocket(URL));
    }, []);
    
    useEffect(() => {
        if (!ws) return;

        ws.onmessage = function(event){
            setData(JSON.parse(event.data));   
        }

        
        ws.onclose = function(event){
                setWs(new WebSocket(URL));
            }
    }, [ws]);

    const changeHandler = (e) => {
        setChosenFile(e.target.files[0]);
    };

    const handleSubmit = (e) => {
        if(!chosenFile) {
            alert("No file chosen!");
            return ;
        }
        setData("");
        const reader = new FileReader();
        reader.readAsText(chosenFile); //async function
        reader.onload = function(event){
            ws.send(reader.result);
        }
    };

    

    if(data === ""){
        return (
            <div className={classes.main}>
            <input type="file" name="file" onChange={changeHandler}/>
            <br/>
            <button onClick={handleSubmit}>Send file</button>
            <br/>
            <h1>Wait For A Moment!</h1>
            </div>
        )
    }

    return (
        <>
        <div className={classes.main}>
            <input type="file" name="file" onChange={changeHandler}/>
            <br/>
            <button onClick={handleSubmit}>Send file</button>
            <br/>
        </div>
        {
            data &&
            <div>{data}</div>
        }
        </>
        
    )
}
export default FileUpload;