import classes from "./ReportLesson.module.css";
import UpdateLesson from "../formUpdates/UpdateLesson";
import { useEffect, useRef, useState, useCallback } from "react";

function ReportLessonHelper(props){
    let lessons = props.data;
    const [result, setResult] = useState(null);
    const finalTable = useRef(null);

    const showLesson = useCallback((lesson) => {
        setResult([<UpdateLesson 
                    key={lesson["lesson_id"]} 
                    lesson={lesson} 
                    groups={props.groups} 
                    teachers={props.teachers} 
                    classrooms={props.classrooms} 
                    />, 
                    finalTable.current]);
    }, [props.groups, props.teachers, props.classrooms]);

    useEffect(() => {
        let rowsForTable = [];
        let newRow = [];
        for(let i=0; i<lessons.length; i++){
            if(i%5 === 0){
                newRow = [];
            }
            let childtable = [];
            for(let j=0; j<lessons[i].length; j++){
                let lesson = lessons[i][j];
                let item = [];
                item.push(<strong key="subject">{lesson["subject_name"]}</strong>);
                item.push(<br key={"s"}></br>);
                item.push(<strong key="topic">{lesson["topic_name"]}</strong>);
                item.push(<br key={"t"}></br>);
                item.push(<strong key="time">{lesson["time"]}</strong>);
    
                if(lesson["teachers"].length > 0){
                    item.push(<br key={"te"}></br>);
                    item.push(<strong key="teacher">Teachers:</strong>);
                    item.push(<br key={"tes"}></br>);
                    item.push(lesson["teachers"][0]);
                    for (let k=1; k<lesson["teachers"].length; k++){
                        item.push(", ");
                        item.push(lesson["teachers"][k]);
                    }
                }
                if(lesson["groups"].length > 0){
                    item.push(<br key={"gr"}></br>);
                    item.push(<strong key="group">Groups:</strong>);
                    item.push(<br key={"grs"}></br>);
                    item.push(lesson["groups"][0]);
                    for (let k=1; k<lesson["groups"].length; k++){
                        item.push(", ");
                        item.push(lesson["groups"][k]);
                    }
                }
    
                item.push(<br key={"cl"}></br>);
                item.push(<strong key="classroom">Classroom:</strong>);
                item.push(<br key={"cls"}></br>);
                item.push(lesson["chosen_classroom"]);
                childtable.push(<tr key={j} onClick={() => showLesson(lesson)}><td key={j}>{item}</td></tr>);
            }
            if(lessons[i].length === 0){
                childtable = (<table className={classes.noData}></table>);
            }
            else{
                childtable = (<table><tbody>{childtable}</tbody></table>);
            }
            if(i%2 === 0){
                newRow.push(<td key={i} className={classes.even}>{childtable}</td>); 
            }   
            else{
                newRow.push(<td key={i} className={classes.odd}>{childtable}</td>); 
            }       
            if(i%5 === 4 || i === lessons.length-1){
                rowsForTable.push(<tr key={(i-i%5)/5}>{newRow}</tr>);
            }  
        }
        finalTable.current = (<table><tbody>{rowsForTable}</tbody></table>);
        setResult(finalTable.current);
    }, [lessons, showLesson]);
      
    return result;
}

export default ReportLessonHelper;