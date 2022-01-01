import { useState } from "react/cjs/react.development";
import LessonFormHelper from "../forms/lessonFormHelper/LessonFormHelper";
import LessonFormInputText from "../forms/lessonFormHelper/LessonFormInputText";
import classess from "./UpdateLesson.module.css";

function UpdateLesson(props){
    const [lessonId, setLessonId] = useState(props.lesson["lesson_id"]);
    const [subjectName, setSubjectName] = useState(props.lesson["subject_name"]);
    const [subjectId, setSubjectId] = useState(props.lesson["subject_id"]);
    const [topicName, setTopicName] = useState(props.lesson["topic_name"]);
    const [topicId, setTopicId] = useState(props.lesson["topic_id"]);
    const [nonpermittedColors, setNonpermittedColors] = useState(props.lesson["nonpermitted_colors"]);

    const [groupName, setGroupName] = useState(props.lesson["groups"]);
    const [groupId, setGroupId] = useState(props.lesson["group_ids"]);
    const [teacherName, setTeacherName] = useState(props.lesson["teachers"]);
    const [teacherId, setTeacherId] = useState(props.lesson["teacher_ids"]);
    const [classroomName, setClassroomName] = useState(props.lesson["classrooms"]);
    const [classroomId, setClassroomId] = useState(props.lesson["classroom_ids"]);

    const handleSubmit = (event) => {
        event.preventDefault();
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
                <br />
            </div>
            
            <LessonFormHelper 
                name="group" 
                itemId={groupId} 
                setItemId={setGroupId}
                itemName={groupName}
                setItemName={setGroupName}
                data={props.groups}
            />

            <LessonFormHelper 
                name="teacher" 
                itemId={teacherId} 
                setItemId={setTeacherId}
                itemName={teacherName}
                setItemName={setTeacherName}
                data={props.teachers}
            />
            
            <LessonFormHelper 
                name="classroom" 
                itemId={classroomId} 
                setItemId={setClassroomId}
                itemName={classroomName}
                setItemName={setClassroomName}
                data={props.classrooms}
            />
            
            <input type="submit" value="Submit lesson" />         
        </form>
    )
}

export default UpdateLesson;