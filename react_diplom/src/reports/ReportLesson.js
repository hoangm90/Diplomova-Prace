import { useState, useEffect, useRef } from "react";
import ReportLessonHelper from "./ReportLessonHelper";
import classes from "./ReportLesson.module.css";

function ReportLesson(props){
    const [lessons, setLessons] = useState(null);
    const [groups, setGroups] = useState(null);
    const [teachers, setTeachers] = useState(null);
    const [classrooms, setClassrooms] = useState(null);
    const [chosenLessons, setChosenLessons] = useState(null);
    const selectedGroup = useRef("all");
    const selectedTeacher = useRef("all");
    const selectedClassroom = useRef("all");

    useEffect(() => {
        fetch("http://localhost:8000/lessons")
        .then(r => r.json())
        .then(d => {setLessons(d); setChosenLessons(d)});
        
        fetch("http://localhost:8000/groups")
        .then(r => r.json())
        .then(d => setGroups(d));

        fetch("http://localhost:8000/teachers")
        .then(r => r.json())
        .then(d => setTeachers(d));

        fetch("http://localhost:8000/classrooms")
        .then(r => r.json())
        .then(d => setClassrooms(d));
    }, []);

    const showItem = (event) => {
        event.preventDefault(); 
        switch(event.target.name){
            case "group": selectedGroup.current = event.target.value; break;
            case "teacher": selectedTeacher.current = event.target.value; break;
            case "classroom": selectedClassroom.current = event.target.value; break;
        }   
        if(selectedTeacher.current === "all" && selectedClassroom === "all" && selectedGroup === "all")
        {
            setChosenLessons(lessons);
        }
        else
        {    
            let chosenLs = [];
            for(let i=0; i<lessons.length; i++)
            {
                let chosen = false;
                let ls = [];
                for(let j=0; j<lessons[i].length; j++)
                {
                    let chosenC = false;
                    let chosenG = false;
                    let chosenT = false;
                    if(selectedClassroom.current === "all" || selectedClassroom.current === lessons[i][j]["chosen_classroom_id"])
                    {
                        chosenC = true;
                    }
                    else {chosenC = false;}
                    if(chosenC)
                    {                      
                        if (selectedGroup.current !== "all")
                        {
                            for(let k=0; k<lessons[i][j]["group_ids"].length; k++)
                            {
                                if(lessons[i][j]["group_ids"][k] === selectedGroup.current){
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
                            for(let k=0; k<lessons[i][j]["teacher_ids"].length; k++)
                            {
                                if(lessons[i][j]["teacher_ids"][k] === selectedTeacher.current){
                                    chosenT = true;
                                    break;
                                }
                            }
                        }
                        else {chosenT = true;}
                    }
                    if(chosenC && chosenG && chosenT){
                        chosen = true;
                        ls.push(lessons[i][j]);
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
                    {groups &&
                        groups.map(elem => {
                            return <option key={elem["group_id"]} value={elem["group_id"]}>
                                    {elem["group_name"]}
                                </option>
                        })}
                </select>

                <select id={"teacher"} name={"teacher"}  onChange={showItem} defaultValue="default">
                    <option disabled value="default"> -- choose teacher -- </option>
                    <option key="all" value="all">All</option>
                    {teachers &&
                        teachers.map(elem => {
                            return <option key={elem["teacher_id"]} value={elem["teacher_id"]}>
                                    {elem["teacher_name"]}
                                </option>
                        })}
                </select>

                <select id={"classroom"} name={"classroom"}  onChange={showItem} defaultValue="default">
                    <option disabled value="default"> -- choose classroom -- </option>
                    <option key="all" value="all">All</option>
                    {classrooms &&
                        classrooms.map(elem => {
                            return <option key={elem["classroom_id"]} value={elem["classroom_id"]}>
                                    {elem["classroom_name"]}
                                </option>
                        })}
                </select>

                <ReportLessonHelper data={chosenLessons} teachers={teachers} groups={groups} classrooms={classrooms}/>
            </>
        );
    }
    return <h1> Wait for a moment</h1>
}

export default ReportLesson;