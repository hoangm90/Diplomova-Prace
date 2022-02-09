import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import LessonForm from './forms/LessonForm';
import SubmitForm from './forms/SubmitForm';

import ReportForm from "./reports/ReportForm";
import ReportLesson from './reports/ReportLesson';

import UpdateForm from './formUpdates/UpdateForm';
import UpdateLesson from './formUpdates/UpdateLesson';

import Layout from "./components/Layout";

function App() {
 
  return (
    <Layout>
        <Routes>
          <Route exact path="/classrooms/form" element={<SubmitForm name="classroom" />} />
          <Route exact path="/groups/form" element={<SubmitForm name="group" />} />
          <Route exact path="/teachers/form" element={<SubmitForm name="teacher" />} />
          <Route exact path="/lessons/form" element={<LessonForm />} />

          <Route exact path="/classrooms/" element={<ReportForm name="classroom" />} />
          <Route exact path="/teachers/" element={<ReportForm name="teacher" />} />
          <Route exact path="/groups/" element={<ReportForm name="group" />} />
          <Route exact path="/lessons/" element={<ReportLesson />} />

          <Route exact path="/classrooms/update" element={<UpdateForm name="classroom" />} />
          <Route exact path="/teachers/update" element={<UpdateForm name="teacher" />} />
          <Route exact path="/groups/update" element={<UpdateForm name="group" />} />
          <Route path="/lessons/:id" element={<UpdateLesson />} />
        </Routes>
        
    </Layout>
  );
};

export default App;