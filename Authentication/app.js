
import { initializeApp } from "https://www.gstatic.com/firebasejs/12.0.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword,onAuthStateChanged,signOut,signInWithEmailAndPassword} from "https://www.gstatic.com/firebasejs/12.0.0/firebase-auth.js";
const firebaseConfig = {
    apiKey: "AIzaSyCHOMHm_XTE1_-oZVloRudi7Fxhs2Ygu_U",
    authDomain: "my-small-farm-system.firebaseapp.com",
    projectId: "my-small-farm-system",
    storageBucket: "my-small-farm-system.firebasestorage.app",
    messagingSenderId: "214056545877",
    appId: "1:214056545877:web:ff1b28273d8f65e70c2edc"
  };

  const app = initializeApp(firebaseConfig);
  const auth = getAuth(app);

  const form = document.getElementById("registerForm");
  const formarea = document.getElementById("form-area");
  const profile = document.getElementById("profile");
  const welcome = document.getElementById("welcome");
  const logout = document.getElementById("logout");
  const loginForm = document.getElementById("loginForm");

    form.addEventListener("submit",(e)=> {
      e.preventDefault();
      const email = form.email.value;
      const password = form.password.value;
      createUserWithEmailAndPassword(auth, email, password)
        .then((result) => {
          alert("User registered successfully!");
        }).catch((error) => {
            alert(error.message);
        })
    })

    onAuthStateChanged(auth, (user) => { 
        //login
      if(user) {
        profile.style.display ="block";
        formarea.style.display ="none";
        welcome.innerText = `Welcome ${user.email}`;
      }else {
        formarea.style.display = "block";
        profile.style.display = "none";
      }
    });
    logout.addEventListener("click", () => {
        signOut(auth).then(() => {
            alert("User logged out successfully!");
        }).catch((error) => {
            alert(error.message);
        });
    });  

    loginForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const email = loginForm.loginEmail.value;
        const password = loginForm.loginPassword.value;
        console.log(email);
        console.log(password);
        //login user
        signInWithEmailAndPassword(auth, email, password)
            .then((userCredential) => {
                alert("User logged in successfully!");
            })
            .catch((error) => {
                alert(error.message);
            });
    });
    