<script setup>
import { ref, onMounted, toRefs } from 'vue';


let csrf_token = ref("");
let successMessage = ref("");
let errorMessage = ref([]);

let facultyOptions = ref([]);
let departmentOptions = ref([]);
let degreeOptions = ref([]);
let statusOptions = ref([]);
let courseOptions = ref([]);
let gradeOptions = ref([]);

let qualificationOptions = ref([]);
let qualSubjectOptions = ref([]);
let qualificationGradeOptions = ref([]);

const courseFields = ref([]);
const gradeFields = ref([]);
const qualificationFields = ref([]);
const subjectFields = ref([]);
const exemptFields = ref([]);
const qualGradeFields = ref([]);

const state = toRefs({ csrf_token, successMessage, errorMessage });

function getCsrfToken() {
  fetch('/api/v1/csrf-token')
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      csrf_token.value = data.csrf_token;
    });
}

function fetchFacultyOptions() {
  fetch('/api/v1/faculties')
    .then(response => response.json())
    .then(data => {
      facultyOptions.value = data;
    })
    .catch(error => {
      console.error(error);
    });
}

function fetchDepartmentOptions() {
  fetch('/api/v1/departments')
    .then(response => response.json())
    .then(data => {
      departmentOptions.value = data;
    })
    .catch(error => {
      console.error(error);
    });
}

function fetchDegreeOptions() {
  fetch('/api/v1/degrees')
    .then(response => response.json())
    .then(data => {
      degreeOptions.value = data;
    })
    .catch(error => {
      console.error(error);
    });
}

function fetchStatusOptions(){
    fetch('/api/v1/status')
        .then(response => response.json())
        .then(data => {
            statusOptions.value= data;
        })
        .catch(error => {
            console.error(error);
        });
}

function fetchCourseOptions() {
  fetch('/api/v1/courses')
    .then(response => response.json())
    .then(data => {
      courseOptions.value = data;
    })
    .catch(error => {
      console.error(error);
    });
}

function fetchGradesOptions(){
    fetch('/api/v1/grades')
        .then(response => response.json())
        .then(data => {
            gradeOptions.value= data;
        })
        .catch(error => {
            console.error(error);
        });
}

function fetchQualificationOptions() {
  fetch('/api/v1/qualifications')
    .then(response => response.json())
    .then(data => {
      qualificationOptions.value = data;
    })
    .catch(error => {
      console.error(error);
    });
}

function fetchSubjectOptions() {
  fetch('/api/v1/qualsubjects')
    .then(response => response.json())
    .then(data => {
      qualSubjectOptions.value = data;
    })
    .catch(error => {
      console.error(error);
    });
}

function fetchQualificationGradesOptions() {
  fetch('/api/v1/qualgrades')
    .then(response => response.json())
    .then(data => {
      qualificationGradeOptions.value = data;
    })
    .catch(error => {
      console.error(error);
    });
}

function newStudentForm() {
    let form = document.querySelector("#newStudentForm")
    let formData = new FormData(form)

    const yearOfStudy = formData.get('yearOfStudy')
    const startYear = formData.get('startYear')

    
    let errors = [];

    if (!yearOfStudy || yearOfStudy.trim() === '') {
        errors.push('Error in Year of Study - This field is required.');
    } else if (![1, 2, 3, 4, 5].includes(parseInt(yearOfStudy))) {
        errors.push('Error - Invalid year of study.');
    }
  

    if (!startYear || startYear.trim() === '') {
        errors.push('Error in Start Year - This field is required.');
    } else if (!/^\d{4}$/.test(startYear)) {
        errors.push('Error in Start Year field - Invalid year format. Please enter a 4-digit integer.');
    }

    if (errors.length > 0) {
        errorMessage.value = errors;
        return;
    }

  

    fetch("/api/v1/students/profile", {
        method: 'POST', 
        body: formData,
        headers: {
            'X-CSRFToken': csrf_token.value,
        }
    })
    .then((response) => {
        if (response.ok) {
            return response.json();
        } else {
            throw response;
        }
    })
    .then((data) => {
        successMessage.value = "Profile successfully created!";
        errorMessage.value = [];
        console.log(data);
    })
    .catch((error) => {
        error.json().then((data) => {
            if (data.errors) {
                errorMessage.value = data.errors;
            } else {
                errorMessage.value = ["An unexpected error occurred."];
            }
            successMessage.value = "";
            console.log(data);
        });
    });
}

// Data properties


onMounted(() => {
  getCsrfToken();
  fetchFacultyOptions();
  fetchDepartmentOptions();
  fetchDegreeOptions();
  fetchStatusOptions();
  fetchCourseOptions();
  fetchGradesOptions();
  fetchQualificationOptions();
  fetchSubjectOptions();
  fetchQualificationGradesOptions();

  addCourseField();
  addGradeField();
  addExemptField();
  addQualificationField();
  addSubjectField();
  addQualGradeField();
});

// Add Course Select Field
function addCourseField() {
  courseFields.value.push('');
}

// Add Grade Select Field
function addGradeField() {
  gradeFields.value.push('');
}

function addExemptField() {
  exemptFields.value.push("");
}

// Add Qualification Select Field
function addQualificationField() {
  qualificationFields.value.push('');
}


// Add Subject Select Field
function addSubjectField() {
  subjectFields.value.push('');
}

// Add Qualification Grade Select Field
function addQualGradeField() {
  qualGradeFields.value.push('');
}


</script>

<template>
  <div class="form-container">
    
    <form @submit.prevent="newStudentForm" id="newStudentForm" method="post" class="form">
      <div class="buttons">
        <button class="btn register" type="submit"><RouterLink class="nav-link"  to="/register">Register</RouterLink></button>
        <button class="btn login" type="submit"><RouterLink class="nav-link"  to="/login">Login</RouterLink></button>
      </div>  
      <p v-if="successMessage" class="alert alert-success">{{ successMessage }}</p>
  
      <div v-if="errorMessage.length">
        <div class="alert alert-danger" v-for="(error, index) in errorMessage" :key="index">
          {{ error }}
        </div>
      </div>
  
      <div class="form-row">
      <div class="col-auto">
        <label for="yearOfStudy">Year of Study:</label>
        <input type="number" id="yearOfStudy" v-model="yearOfStudy"  class="form-control">
      </div>

      <div class="col-auto">
        <label for="faculty">Select your faculty:</label>
        <select id="faculty" v-model="faculty" class="form-control">
          <option v-for="facultyOption in facultyOptions" :value="facultyOption">{{ facultyOption }}</option>
        </select>
      </div>

      <div class="col-auto">
        <label for="department">Department:</label>
        <select id="department" v-model="department"  class="form-control">
          <option v-for="departmentOption in departmentOptions" :value="departmentOption">{{ departmentOption }}</option>
        </select>
      </div>
    </div>
  
      <div class="form-group">
        <label for="degree">Select your Degree:</label>
        <select id="degree" v-model="degree"  class="form-control">
          <option v-for="degreeOption in degreeOptions" :value="degreeOption">{{ degreeOption }}</option>
        </select>
      </div>
  
      <div class="form-group">
        <label for="status">Status:</label>
        <select id="status" v-model="status" class="form-control">
          <option v-for="statusOption in statusOptions" :value="statusOption">{{ statusOption }}</option>
        </select>
      </div>
  
      <div class="form-group">
        <label for="startYear">Enter the year you started your degree:</label>
        <input type="number" id="startYear" v-model="startYear" class="form-control">
      </div>
  
      <div class="form-group">
        <label for="courses">Select the courses you have completed/currently taking:</label>
        <div v-for="(courseField, index) in courseFields" :key="index">
          <input type="text" v-model="courseFields[index]" list="courseOptions" placeholder="Type a course" class="form-control">
          <datalist id="courseOptions">
            <option v-for="courseOption in courseOptions" :value="courseOption">{{ courseOption }}</option>
          </datalist>
        </div>
        <button type="button" @click="addCourseField" class="btn btn-secondary">Add Course</button>
      </div>
  
      <div class="form-group">
        <label for="grades">Letter Grade:</label>
        <div v-for="(gradeField, index) in gradeFields" :key="index">
          <select v-model="gradeFields[index]" class="form-control">
            <option v-for="gradeOption in gradeOptions" :value="gradeOption">{{ gradeOption }}</option>
          </select>
        </div>
        <button type="button" @click="addGradeField" class="btn btn-secondary">Add Grade</button>
      </div>
  
      <div class="form-group">
        <label for="gpa">GPA:</label>
        <input type="number" id="gpa" v-model="gpa" min="0" max="4.3" step="0.01" class="form-control">
      </div>
  
      <div class="form-group">
        <label for="desiredGpa">Desired GPA:</label>
        <input type="number" id="desiredGpa" v-model="desiredGpa" min="0" max="4.3" step="0.01" class="form-control">
      </div>
  
      <div class="form-group">
        <label for="exemptFrom">Exempted Courses:</label>
        <div v-for="(exemptField, index) in exemptFields" :key="index">
          <input type="text" v-model="exemptFields[index]" list="courseOptions" placeholder="Type an exempted course" class="form-control">
          <datalist id="courseOptions">
            <option v-for="courseOption in courseOptions" :value="courseOption">{{ courseOption }}</option>
          </datalist>
        </div>
        <button type="button" @click="addExemptField" class="btn btn-secondary">Add Exempted Course</button>
      </div>
  
      <div class="form-group">
        <label for="qualifications">Select the type of qualifications you have obtained:</label>
        <div v-for="(qualificationField, index) in qualificationFields" :key="index">
          <select v-model="qualificationFields[index]" class="form-control">
            <option v-for="qualificationOption in qualificationOptions" :value="qualificationOption">{{ qualificationOption }}</option>
          </select>
        </div>
        <button type="button" @click="addQualificationField" class="btn btn-secondary">Add Qualification</button>
      </div>
  
      <div class="form-group">
        <label for="qualSubjects">Select the Subject of prerequisite qualifications you have obtained:</label>
        <div v-for="(subjectField, index) in subjectFields" :key="index">
          <select v-model="subjectFields[index]" class="form-control">
            <option v-for="qualSubjectOption in qualSubjectOptions" :value="qualSubjectOption">{{ qualSubjectOption }}</option>
          </select>
        </div>
        <button type="button" @click="addSubjectField" class="btn btn-secondary">Add Subject</button>
      </div>
  
      <div class="form-group">
        <label for="qualgrades">Select the appropriate grade of prerequisite qualifications you have obtained:</label>
        <div v-for="(qualGradeField, index) in qualGradeFields" :key="index">
          <select v-model="qualGradeFields[index]" class="form-control">
            <option v-for="qualificationGradeOption in qualificationGradeOptions" :value="qualificationGradeOption">{{ qualificationGradeOption }}</option>
          </select>
        </div>
        <button type="button" @click="addQualGradeField" class="btn btn-secondary">Add Qualification Grade</button>
      </div>
  
      <button type="submit" class="btn btn-primary">Submit</button>
    </form>
  </div>

  </template>
  

<style>

.form-container {
    width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }

  .login {
  background-color: rgb(11, 126, 192);
  margin-left: 5px;
  width: 200px;
  color: white;
}

.register {
  background-color: rgb(150, 247, 4);
  margin-right: 15px;
  width: 200px;
  color: white;
}

.login:hover {
  background-color: #0b7ec0;
}

.register:hover {
  background-color: #5fdf5f;
}

.buttons {
  display: flex;
  margin-bottom: 5px;
  padding: 5px;
  
  
}

</style>
