import { useState, useEffect } from "react";
import classess from "./LessonForm.module.css"
import LessonFormHelper from "./lessonFormHelper/LessonFormHelper";
import LessonFormInputText from "./lessonFormHelper/LessonFormInputText";

function LessonForm(){
    const [dataGroup, setDataGroup] = useState(null);
    const [dataTeacher, setDataTeacher] = useState(null);
    const [dataClassroom, setDataClassroom] = useState(null);

    const [lessonId, setLessonId] = useState("");
    const [subjectName, setSubjectName] = useState("");
    const [subjectId, setSubjectId] = useState("");
    const [topicName, setTopicName] = useState("");
    const [topicId, setTopicId] = useState("");
    const [nonpermittedColors, setNonpermittedColors] = useState("");

    const [groupName, setGroupName] = useState([]);
    const [groupId, setGroupId] = useState([]);
    const [teacherName, setTeacherName] = useState([]);
    const [teacherId, setTeacherId] = useState([]);
    const [classroomName, setClassroomName] = useState([]);
    const [classroomId, setClassroomId] = useState([]);

    useEffect(() => {
        fetch("http://localhost:8000/groups")
        .then(r => r.json())
        .then(d => setDataGroup(d));

        fetch("http://localhost:8000/teachers")
        .then(r => r.json())
        .then(d => setDataTeacher(d));

        fetch("http://localhost:8000/classrooms")
        .then(r => r.json())
        .then(d => setDataClassroom(d));
    }, []);

    const handleSubmit = (event) => {
        event.preventDefault();

        const newLesson = {
            "lesson": {
                "lesson_id": lessonId,
                "subject_id": subjectId,
                "subject_name": subjectName,
                "topic_id": topicId,
                "topic_name": topicName,
                "master_id": "",
                "color": "-1",
                "chosen_classroom": "",
                "time": "",
                "nonpermitted_colors": nonpermittedColors,
            },
            "group_ids": groupId,
            "teacher_ids": teacherId,
            "classroom_ids": classroomId,
        };
        console.log(newLesson);
        fetch("http://localhost:8000/lessons", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(newLesson)
        }).then((response) => {
            if(response.ok){
                alert("Submit lesson successfully!");
            }
            else{
                alert("Something went wrong!");
            }
        });

        setLessonId("");
        setSubjectId("");
        setSubjectName("");
        setTopicId("");
        setTopicName("");
        setNonpermittedColors("");

        setGroupId([]);
        setGroupName([]);
        setTeacherId([]);
        setTeacherName([]);
        setClassroomId([]);
        setClassroomName([]);
    }

    return (
        <form onSubmit={handleSubmit}>
            <h1>SUBMIT LESSON</h1>
            <div className={classess.lesson}>
                <LessonFormInputText name="lesson ID" item={lessonId} setItem={setLessonId}/> 
                <br />
                <LessonFormInputText name="subject ID" item={subjectId} setItem={setSubjectId}/>
                <br />
                <LessonFormInputText name="subject name" item={subjectName} setItem={setSubjectName}/>
                <br />
                <LessonFormInputText name="topic ID" item={topicId} setItem={setTopicId}/>
                <br />
                <LessonFormInputText name="topic name" item={topicName} setItem={setTopicName}/>
                <br />
                <LessonFormInputText name="nonpermitted intervals" item={nonpermittedColors} setItem={setNonpermittedColors}/>
            </div>
            
            <LessonFormHelper 
                name="group" 
                itemId={groupId} 
                setItemId={setGroupId}
                itemName={groupName}
                setItemName={setGroupName}
                data={dataGroup}
            />

            <LessonFormHelper 
                name="teacher" 
                itemId={teacherId} 
                setItemId={setTeacherId}
                itemName={teacherName}
                setItemName={setTeacherName}
                data={dataTeacher}
            />
            
            <LessonFormHelper 
                name="classroom" 
                itemId={classroomId} 
                setItemId={setClassroomId}
                itemName={classroomName}
                setItemName={setClassroomName}
                data={dataClassroom}
            />
            
            <input type="submit" value="Submit lesson" />         
        </form>
    )
}

export default LessonForm;