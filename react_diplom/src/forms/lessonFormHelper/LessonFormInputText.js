function LessonFormInputText(props){
    return (
        <label>Enter {props.name}: 
                <input 
                type="text"
                name={props.name}
                value={props.item}
                onChange={(e) => {props.setItem(e.target.value)}}
                />
        </label>
    );
}
export default LessonFormInputText;