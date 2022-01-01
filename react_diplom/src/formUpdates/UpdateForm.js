import { useState, useEffect, useRef } from "react";
import classess from "./UpdateForm.module.css"

function UpdateForm(props){
    const [data, setData] = useState(null);
    const [queryId, setQueryId] = useState("");
    const [item, setItem] = useState(null);
    const todo = useRef("");
    const url = "http://localhost:8000/" + props.name + "s";
    const itemAttributeName = props.name + "_name";
    const itemAttributeId = props.name + "_id";
    const valueUpdateButton = "UPDATE " + props.name.toUpperCase();
    const valueDeleteButton = "DELETE " + props.name.toUpperCase();

    useEffect(() => {
        fetch(url)
        .then(r => r.json())
        .then(d => setData(d));
        setItem(null);
        setQueryId("");
    }, [props.name, url]);

    const showItem = (event) => {
        setQueryId(event.target.value)
        for (let i=0; i<data.length; i++){
            if (data[i][itemAttributeId] === event.target.value){
                setItem({
                    "id": data[i][itemAttributeId], 
                    "name": data[i][itemAttributeName],    
                    "nonpermitted_colors": data[i]["nonpermitted_colors"] != null ? data[i]["nonpermitted_colors"] : "",            
                });
                break;
            }
        }
    }

    const handleSubmit = (event) => {
        event.preventDefault();
        let urlQuery = "http://localhost:8000/" + props.name + "s?" + itemAttributeId + "=" + queryId;
        if (todo.current === "update")
        {
            fetch(urlQuery, {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(item)
            }).then((response) => {
                if(response.ok){
                    alert("Update successfully!");
                }
                else {
                    alert("Something went wrong!");
                }
            })
            .then(() => fetch(url))
            .then(r => r.json())
            .then(d => setData(d));
        }
        else if (todo.current === "delete")
        {
            fetch(urlQuery, {
                method: "DELETE",
            }).then((response) => {
                if(response.ok){
                    alert("Delete sucessfully!");
                }
                else {
                    alert("Something went wrong!");
                }
            })
            .then(() => fetch(url))
            .then(r => r.json())
            .then(d => setData(d));
        }

        setItem(null);
        setQueryId("");
        todo.current = "";
        
    }

    return (
        <form onSubmit={handleSubmit}>
            <h1>{props.name.toUpperCase()} UPDATE</h1>
            <label>Choose the {props.name} to update: <br />
                <select id={props.name} name={props.name} onChange={showItem} value="default">
                    <option disabled value="default"> -- select an option -- </option>
                    {data &&
                        data.map(elem => {
                            return <option key={elem[itemAttributeId]} value={elem[itemAttributeId]}>
                                    {elem[itemAttributeName]}
                                </option>
                        })}
                </select>
            </label>
            {item &&
            <>
                <h1>Chosen {props.name}'s information:</h1>  
                <label> Name:
                    <input type="text" value={item["name"]} 
                        onChange={(e) => {setItem(prevState => ({
                            ...prevState,
                            "name": e.target.value
                        }))}}
                    />
                </label>
                <label> ID:
                    <input type="text" value={item["id"]} 
                        onChange={(e) => {setItem(prevState => ({
                            ...prevState,
                            "id": e.target.value
                        }))}}
                    />
                </label>
                <label> NONPERMITTED INTERVALS:
                    <input type="text" value={item["nonpermitted_colors"]} 
                        onChange={(e) => {setItem(prevState => ({
                            ...prevState,
                            "nonpermitted_colors": e.target.value
                        }))}}
                    />
                </label>
                <input type="submit" value={valueUpdateButton} onClick={() => todo.current = "update"}/>
                <input type="submit" value={valueDeleteButton} onClick={() => todo.current = "delete"}/>
            </>
            }
        </form>
    )
}

export default UpdateForm;