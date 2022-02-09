import { Link } from "react-router-dom";
import classes from "./NavigationBar.module.css"

function NavigationBar(){
    return (
        <ul>
            <li className={classes.dropdown}>
                <Link to="/classrooms">Classroom</Link>
                <div className={classes.dropdowncontent}>
                    <Link to="/classrooms">Classrooms</Link>
                    <Link to="/classrooms/form">Submit classroom</Link>
                    <Link to="classrooms/update">Update classroom</Link>
                </div> 
            </li>

            <li className={classes.dropdown}>
                <Link to="/groups">Group</Link>
                <div className={classes.dropdowncontent}>
                    <Link to="/groups">Groups</Link>
                    <Link to="/groups/form">Submit group</Link>
                    <Link to="groups/update">Update group</Link>
                </div>
            </li>

            <li className={classes.dropdown}>
                <Link to="/teachers">Teacher</Link>
                <div className={classes.dropdowncontent}>
                    <Link to="/teachers">Teachers</Link>
                    <Link to="/teachers/form">Submit teacher</Link>
                    <Link to="teachers/update">Update teacher</Link>
                </div>
            </li>

            <li className={classes.dropdown}>
                <Link to="lessons">Lesson</Link>
                <div className={classes.dropdowncontent}> 
                    <Link to="/lessons">Lessons</Link>
                    <Link to="/lessons/form">Lesson Form</Link>
                </div>
            </li>
        </ul>
         
    )
}

export default NavigationBar;