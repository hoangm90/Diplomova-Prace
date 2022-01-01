import { useState, useEffect } from "react";
import classes from "./ReportForm.module.css";

function ReportForm(props){
    const [data, setData] = useState(null);
    const url = "http://localhost:8000/"+ props.name + "s";
    const itemAttributeName = props.name + "_name";
    const itemAttributeId = props.name + "_id";

    useEffect(() => {
        setData(null);
        fetch(url)
        .then(r => r.json())
        .then(d => setData(d));
    }, [props.name, url]);

    if (data){
        return (
            <table>
                <thead>
                    <tr>
                        <th>{props.name.toUpperCase()} NAME</th>
                        <th>{props.name.toUpperCase()} ID</th>
                        <th>NONPERMITTED INTERVALS</th>
                    </tr>
                </thead>
                <tbody>
                    {data &&
                        data.map((item) => {
                        return (
                            <tr key={item[itemAttributeId]}>
                                <td>{item[itemAttributeName]}</td>
                                <td>{item[itemAttributeId]}</td>
                                <td>{item["nonpermitted_colors"]}</td>
                            </tr>
                        );
                        })}
                </tbody>
            </table>
        )
    }
    return <h1> Wait for a moment</h1>
    
}

export default ReportForm;