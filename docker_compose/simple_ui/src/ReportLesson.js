import { useState, useRef } from "react";
import ReportLessonHelper from "./ReportLessonHelper";
import classes from "./ReportLesson.module.css";

function ReportLesson(props){
    const [chosenLessons, setChosenLessons] = useState(props.lessons);
    const selectedGroup = useRef("all");
    const selectedTeacher = useRef("all");
    const selectedClassroom = useRef("all");

    const showItem = (event) => {
        event.preventDefault(); 
        switch(event.target.name){
            case "group": selectedGroup.current = event.target.value; break;
            case "teacher": selectedTeacher.current = event.target.value; break;
            case "classroom": selectedClassroom.current = event.target.value; break;
        }   
        if(selectedTeacher.current === "all" && selectedClassroom.current === "all" && selectedGroup.current === "all")
        {
            setChosenLessons(props.lessons);
        }
        else
        {    
            let chosenLs = [];
            for(let sameTimeLesson of props.lessons)
            {
                let chosen = false;
                let ls = [];
                for(let lesson of sameTimeLesson)
                {
                    let chosenC = false;
                    let chosenG = false;
                    let chosenT = false;
                    if(selectedClassroom.current === "all" || selectedClassroom.current === String(lesson["chosenClassroomId"]))
                    {
                        chosenC = true;
                    }
                    else {chosenC = false;
                    }
                    if(chosenC)
                    {                      
                        if (selectedGroup.current !== "all")
                        {
                            for(let gr of lesson["groupsIds"])
                            {
                                if(String(gr) === selectedGroup.current){
                                    chosenG = true;
                                    break;
                                }
                            }
                        }
                        else {chosenG = true;}
                    }
                    if(chosenC && chosenG)
                    {                      
                        if (selectedTeacher.current !== "all")
                        {
                            for(let te of lesson["teachersIds"])
                            {
                                if(String(te) === selectedTeacher.current){
                                    chosenT = true;
                                    break;
                                }
                            }
                        }
                        else {chosenT = true;}
                    }
                    if(chosenC && chosenG && chosenT){
                        chosen = true;
                        ls.push(lesson);
                    }
                }
                if(chosen){
                    chosenLs.push(ls);
                }
                else {
                    chosenLs.push([]);
                }
            }
            setChosenLessons(chosenLs);
        }
    }

    if(chosenLessons){
        return (
            <>
                <select id={"group"} name={"group"}  onChange={showItem} defaultValue="default">
                    <option disabled value="default"> -- choose group -- </option>
                    <option key="all" value="all">All</option>
                    {props.groups &&
                        props.groups.map(elem => {
                            return <option key={elem["id"]} value={elem["id"]}>
                                    {elem["name"]}
                                </option>
                        })}
                </select>

                <select id={"teacher"} name={"teacher"}  onChange={showItem} defaultValue="default">
                    <option disabled value="default"> -- choose teacher -- </option>
                    <option key="all" value="all">All</option>
                    {props.teachers &&
                        props.teachers.map(elem => {
                            return <option key={elem["id"]} value={elem["id"]}>
                                    {elem["name"]}
                                </option>
                        })}
                </select>

                <select id={"classroom"} name={"classroom"}  onChange={showItem} defaultValue="default">
                    <option disabled value="default"> -- choose classroom -- </option>
                    <option key="all" value="all">All</option>
                    {props.classrooms &&
                        props.classrooms.map(elem => {
                            return <option key={elem["id"]} value={elem["id"]}>
                                    {elem["name"]}
                                </option>
                        })}
                </select>

                <ReportLessonHelper data={chosenLessons} />
            </>
        );
    }
    return <h1> Wait for a moment</h1>
}

export default ReportLesson;