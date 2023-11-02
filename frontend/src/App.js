import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [assignedStudents, setAssignedStudents] = useState(null);
  const [mentors, setMentors] = useState([]);
  const [notAssignedStudents, setNotAssignedStudents] = useState(null);
  // localStorage.clear();
  const [currentMentor, setCurrentMentor] = useState(() => localStorage.getItem('currentMentor') || null);
  const [selectedStudent,setSelectedStudent]=useState(null)
  const [filterType,setFilterType]=useState(null)


  const fetchAssignedStudents = async () => {
    const endpoint = `http://localhost:8000/api/mentor/${currentMentor[0]}`;
    try {
      const response = await axios.get(endpoint);
      // console.log(response.data.assigned_students);
      const data={
        "student_ids":response.data.assigned_students
      }
      const url="http://localhost:8000/api/select-students/"
      const res=await axios.post(url,data);
      setAssignedStudents(res.data)
      // console.log(res.data);
    } catch (error) {
      console.error(error);
    }
  }
  const fetchNotAssignedStudents = async () => {
    const endpoint = `http://localhost:8000/api/unassigned`;
    try {
      const response = await axios.get(endpoint);
      
      setNotAssignedStudents(response.data);
    } catch (error) {
      console.error(error);
    }
  }
  useEffect(() => {
    const fetchMentors = async () => {
      const endpoint = "http://localhost:8000/api/mentor";
      try {
        const response = await axios.get(endpoint);
        setMentors(response.data);
      } catch (error) {
        console.error(error);
      }
    }
    if (currentMentor === null) {
      fetchMentors();
    }
  }, [currentMentor]);

  useEffect(() => {
    

    

    if (currentMentor !== null) {
      fetchAssignedStudents();
      fetchNotAssignedStudents();
    }
  }, [currentMentor]);

  const changeMentor = () => {
    const mentorListElement = document.getElementById("mentor-list");
    const data = mentorListElement.value;
    setCurrentMentor(data);
    localStorage.setItem('currentMentor', data);
  };
  const clearMentor=()=>
  {
    localStorage.clear();
    setCurrentMentor(null);
  }
  const saveMarkToDb=async(id,sub1,sub2,sub3)=>
  {
    const data= {
        "student_id": id,
        "mentor_id":currentMentor,
        "sub1": sub1,
        "sub2": sub2,
        "sub3": sub3,
    }
    const url="http://localhost:8000/api/save-marks/"
    try{
      const response =await axios.post(url,data);
    }
    catch(e)
    {
      console.log("error in saving marks",e);
    
    }
}
  const saveMarksHandler=(event)=>
  {
    const element = event.target;
    const parent = element.parentNode;
    // console.log(parent);
    const subpar=parent.querySelector('.sub-head').querySelector('.sub1');
    const sub1 = parent.querySelector('.sub-head').querySelector('.sub1').value || 0; // Default to 0 if value is null or undefined
    const sub2 = parent.querySelector('.sub-head').querySelector('.sub2').value || 0; // Default to 0 if value is null or undefined
    const sub3 = parent.querySelector('.sub-head').querySelector('.sub3').value || 0; // Default to 0 if value is null or undefined
    
    const id=parseInt(parent.value);
    saveMarkToDb(id,parseInt(sub1),parseInt(sub2),parseInt(sub3));
  }
  const lockMarksInDb=async(id,sub1,sub2,sub3)=>
  {
  const data= {
      "student_id": id,
      "mentor_id":currentMentor,
      "sub1": sub1,
      "sub2": sub2,
      "sub3": sub3,
    }
  const url="http://localhost:8000/api/submit-marks/"
  try{
    const response =await axios.post(url,data);
    fetchAssignedStudents();

  }
  catch(e)
  {
    console.log("error in saving marks",e);
  }    
  }
  const marksLockHandler=(event)=>
  {
    const element = event.target;
    const parent = element.parentNode;
    const sub1 = parent.querySelector('.sub1').value || 0; // Default to 0 if value is null or undefined
    const sub2 = parent.querySelector('.sub2').value || 0; // Default to 0 if value is null or undefined
    const sub3 = parent.querySelector('.sub3').value || 0; // Default to 0 if value is null or undefined
    
    const id=parseInt(parent.value);
    lockMarksInDb(id,sub1,sub2,sub3);

  }
  const changeTotal = (event) => {
    const element = event.target;
    const parent = element.parentNode;
    const sub1 = parent.querySelector('.sub1').value || 0; // Default to 0 if value is null or undefined
    const sub2 = parent.querySelector('.sub2').value || 0; // Default to 0 if value is null or undefined
    const sub3 = parent.querySelector('.sub3').value || 0; // Default to 0 if value is null or undefined
    const total = parent.parentNode.querySelector('.subTotal').querySelector('.total');

  
    // Calculate the total value based on sub1, sub2, and sub3
    const totalValue = parseInt(sub1) + parseInt(sub2) + parseInt(sub3);
    console.log("total",totalValue)
    // Update the total input field
    total.value = isNaN(totalValue) ? '' : totalValue.toString();
  };
  const removeStudentFromDb=async(id)=>
  {
    const endpoint = 'http://localhost:8000/api/remove-student/';
    try {
      const data={
        "student_id": id,
        "mentor_id":currentMentor[0]
    }
    // console.log(data);
      const response = await axios.post(endpoint,data);
      if(response.data.alert)
      {
        alert(response.data.alert)
      }
      fetchAssignedStudents();
      fetchNotAssignedStudents();
      // setNot
    
    } catch (error) {
      console.error(error);
    }
  }
  
  const removeStudent=(event)=>
  {
    const element = event.target;
    const parent = element.parentNode;
    // console.log(parent);
    const id=parseInt(parent.value);
    removeStudentFromDb(id);
    // fetchAssignedStudents();
  }
  const addStudentinDb=async(id)=>{
    try{
      const url="http://localhost:8000/api/add-student/"
      const data={
        "student_id": id,
        "mentor_id":parseInt(currentMentor.split(',')[0])
      }
      const response=await axios.post(url,data);
      fetchAssignedStudents();
      fetchNotAssignedStudents();
      if(response.data.alert)
      {
        alert(response.data.alert)
      }
    }
    catch(e)
    {
      console.log("error adding student",e);
    }
  }
  const addStudent=(event)=>
  {
    addStudentinDb(event.target.value);
  }
  if (currentMentor && assignedStudents) {
    return <div>
      <div className='navbar'>
        <div className='name-holder'>
          {
            currentMentor.split(',')[1]
          }
        </div>
        <button className='navbar-logout' onClick={clearMentor}>Switch</button>
      </div>
      <div className='bottom-page'>
        <div className='left-part'>
          <div className='left-part-filter'>
            <div className={`${filterType===null ? "leftSelected" : "leftUnselected"}`}
                  onClick={()=>setFilterType(null)}
            >
              ALL
            </div>
            <div className={`${filterType==='1' ? "leftSelected" : "leftUnselected"}`}
                  onClick={()=>setFilterType("1")}
            >
              Evaluate
            </div>
            <div className={`${filterType==='2' ? "leftSelected" : "leftUnselected"}`}
                  onClick={()=>setFilterType("2")}
            >
              Submitted
            </div>
          </div>
          {
            assignedStudents?.map((student, index)=>
            (
              
              
              (filterType===null||(filterType==='1'&& student.locked===false)||(filterType==='2' && student.locked===true))?(<li className="student-list" key={index} value={student.student}>
                <div className='student-list-name'>{student.student_name}</div>
                
                <div className='sub-head'>
                  <label className='subhead'>Sub 1 : </label>
                  <input type='number' className='sub sub1' defaultValue={student.sub1} onChange={changeTotal} disabled={student.locked}></input>
                  <label className='subhead'>Sub 2 : </label>
                  <input type='number' className='sub sub2' defaultValue={student.sub2} onChange={changeTotal} disabled={student.locked}></input>
                  <label className='subhead'>Sub 3 : </label>
                  <input type='number' className='sub sub3' defaultValue={student.sub3} onChange={changeTotal} disabled={student.locked}></input>
                </div>
                <div>
                  <div className='subTotal'>
                    Total :
                    <input type='number' className='total' defaultValue={student.total} disabled></input>
                  </div>
                </div>
                
                <br/>
                {
                  student.locked===false?<button className='cta' onClick={saveMarksHandler}>Save</button>:null
                }
                {
                  student.locked===false?<button className='cta' onClick={marksLockHandler}>Submit</button>:null
                }
                <button  className='cta' onClick={removeStudent}>Remove</button>
              </li>):null
            ))
          }
        </div>
        <div className='right-bar'>
          <div className='right-head'>Unassigned Students</div>
          <div className="scrollable-list">
            {notAssignedStudents.map((student, index) => (
              <div 
                className={selectedStudent === student.id ? 'selected-student' : 'scrollable-list-child'} 
                key={index}
                 // don't forget to add a 'key' prop when mapping
                onClick={() => setSelectedStudent(student.id)}
                onMouseEnter={() => setSelectedStudent(student.id)}
                onMouseLeave={() => setSelectedStudent(null)}
              >
                {student.name}
                <button className='add-student-btn' value={student.id} onClick={addStudent}>+</button>
              </div>
            ))}
          </div>

        </div>
      </div>
    </div>;
  }

  if (mentors.length > 0) {
    return (
      <div className='popup-background'>
        <div className='popup-foreground'>
          <label htmlFor="mentor-list">Choose a Mentor:</label>
          <div className='mentor-select'>
            <select id="mentor-list" className='mentor-list'>
              {mentors.map((mentor, index) => (
                <option key={mentor.id} value={[mentor.id,mentor.name]}>{mentor.name}</option>
              ))}
            </select>
            <button className='submit' onClick={changeMentor}>Select</button>
          </div>
        </div>
      </div>
    );
  }

  return <></>;
}

export default App;
