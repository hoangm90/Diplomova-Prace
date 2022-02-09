import classes from './Layout.module.css';
import NavigationBar from './NavigationBar';

function Layout(props){
    return <div>
        <div className={classes.fixBar}>
            <NavigationBar />
        </div>
        <main className={classes.main}>
            {props.children}
        </main>
    </div>
}

export default Layout;