import { useEffect, useState } from "react";
import classes from "./SubmitForm.module.css"

function SubmitForm(props){
    const [ itemName, setItemName] = useState("");
    const [ itemId, setItemId] = useState("");
    const [ nonpermittedColors, setNonpermittedColors] = useState("");
    const submitButtonValue = "SUBMIT " + props.name.toUpperCase();

    useEffect(() => {
        setItemId("");
        setItemName("");
        setNonpermittedColors("");
    }, [props.name]);

    const handleSubmit = (event) => {
        event.preventDefault();
        const url = "http://localhost:8000/" + props.name + "s";

        const newItem = {
            "id": itemId,
            "name": itemName,
            "nonpermitted_colors": nonpermittedColors,
        };

        
        fetch(url, {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(newItem)
        }).then((response) => {
            if(response.ok){
                alert("Submit successfully!");
            }
            else {
                alert("Something went wrong!");
            }
        });
        setItemName("");
        setItemId("");
        setNonpermittedColors("");
    }

    return (
        <div>
            <form onSubmit={handleSubmit}>
                <h1 className={classes.title}>SUBMIT {props.name.toUpperCase()}</h1>
                <label>Enter {props.name} name: 
                    <input 
                    type="text"
                    name="itemName"
                    value={itemName}
                    onChange={(e) => {setItemName(e.target.value)}}
                    />
                </label>
                <br />
                <label>Enter {props.name} ID: 
                    <input 
                    type="text"
                    name="itemId"
                    value={itemId}
                    onChange={(e) => {setItemId(e.target.value)}}
                    />
                </label>
                <br />
                <label>Enter {props.name} nonpermitted intervals: 
                    <input 
                    type="text"
                    name="nonpermittedColors"
                    value={nonpermittedColors}
                    onChange={(e) => {setNonpermittedColors(e.target.value)}}
                    />
                </label>
                <br />
                <input type="submit" value={submitButtonValue}/>
            </form>
        </div>
    )
}

export default SubmitForm;