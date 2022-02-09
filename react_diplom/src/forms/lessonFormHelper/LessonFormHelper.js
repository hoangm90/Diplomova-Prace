import classess from "../LessonForm.module.css"

function LessonFormHelper(props){
    let iId = props.name + "_id";
    let iName = props.name + "_name";
    const addItem = (event) => {
        const val = event.target.value.split(",");
        let needAdding = true;
        for(let i=0; i<props.itemId.length; i++)
        {
            if(props.itemId[i] === val[0]){
                needAdding = false;
                break;
            }
        }
        if( val.length > 2){
            val[1] = val[1] + "," + val[2];
        }

        if (needAdding)
        {
            props.setItemId([...props.itemId, val[0]]);
            props.setItemName([...props.itemName, val[1]]);
        } 
        else {
            props.setItemId(props.itemId.filter(id => id !== val[0]));
            props.setItemName(props.itemName.filter(name => name !== val[1]));
        }
    }
    return (
        <div className={classess.lesson}>
            <br />
            <label>Chosen {props.name}s:
                <input 
                    type="text"
                    name={props.name+"Name"}
                    value={props.itemName.join(", ")}
                    readOnly
                />
            </label>
            <br />
            <label>Chose next {props.name}:
                <select id={props.name} name={props.name} onChange={addItem} value={"default"}>
                <option disabled value="default"> -- select an option -- </option>
                {props.data &&
                    props.data.map((item) => {
                    return (
                        <option key={item[iId]} value={[item[iId], item[iName]]}>
                            {item[iName]}
                        </option>
                    );
                })}
                </select>
            </label>
        </div>
    )
}

export default LessonFormHelper;