<!DOCTYPE html>
<!--[if IE 7]>
<html class="ie ie7 no-js" lang="en-US">
<![endif]-->
<!--[if IE 8]>
<html class="ie ie8 no-js" lang="en-US">
<![endif]-->
<!--[if !(IE 7) | !(IE 8)  ]><!-->
<html lang="en" class="no-js">

<!-- moviegrid_light16:30-->
<head>
	<!-- Basic need -->
	<title>Help360 | History</title>
	<meta charset="UTF-8">
	<meta name="description" content="">
	<meta name="keywords" content="">
	<meta name="author" content="">
	<link rel="profile" href="#">

    <!--Google Font-->
    <link rel="stylesheet" href='http://fonts.googleapis.com/css?family=Dosis:400,700,500|Nunito:300,400,600' />
	<!-- Mobile specific meta -->
	<meta name=viewport content="width=device-width, initial-scale=1">
	<meta name="format-detection" content="telephone-no">

	<!-- CSS files -->
	<link rel="stylesheet" href="{{asset('dashboard/css/plugins.css')}}">
	<link rel="stylesheet"  href="{{asset('dashboard/css/style.css')}}">

	

</head>
<body>

<!--login form popup-->
<div class="login-wrapper" id="login-content">
    <div class="login-content">
        <a href="#" class="close">x</a>
        <h3>Login</h3>
        <form method="post" action="#">
        	<div class="row">
        		 <label for="username">
                    Username:
                    <input type="text" name="username" id="username" placeholder="Hugh Jackman" pattern="^[a-zA-Z][a-zA-Z0-9-_\.]{8,20}$" required="required" />
                </label>
        	</div>
           
            <div class="row">
            	<label for="password">
                    Password:
                    <input type="password" name="password" id="password" placeholder="******" pattern="(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$" required="required" />
                </label>
            </div>
            <div class="row">
            	<div class="remember">
					<div>
						<input type="checkbox" name="remember" value="Remember me"><span>Remember me</span>
					</div>
            		<a href="#">Forget password ?</a>
            	</div>
            </div>
           <div class="row">
           	 <button type="submit">Login</button>
           </div>
        </form>
        <div class="row">
        	<p>Or via social</p>
            <div class="social-btn-2">
            	<a class="fb" href="#"><i class="ion-social-facebook"></i>Facebook</a>
            	<a class="tw" href="#"><i class="ion-social-twitter"></i>twitter</a>
            </div>
        </div>
    </div>
</div>
<!--end of login form popup-->
<!--signup form popup-->
<div class="login-wrapper"  id="signup-content">
    <div class="login-content">
        <a href="#" class="close">x</a>
        <h3>sign up</h3>
        <form method="post" action="#">
            <div class="row">
                 <label for="username-2">
                    Username:
                    <input type="text" name="username" id="username-2" placeholder="Hugh Jackman" pattern="^[a-zA-Z][a-zA-Z0-9-_\.]{8,20}$" required="required" />
                </label>
            </div>
           
            <div class="row">
                <label for="email-2">
                    your email:
                    <input type="password" name="email" id="email-2" placeholder="" pattern="(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$" required="required" />
                </label>
            </div>
             <div class="row">
                <label for="password-2">
                    Password:
                    <input type="password" name="password" id="password-2" placeholder="" pattern="(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$" required="required" />
                </label>
            </div>
             <div class="row">
                <label for="repassword-2">
                    re-type Password:
                    <input type="password" name="password" id="repassword-2" placeholder="" pattern="(?=^.{8,}$)((?=.*\d)|(?=.*\W+))(?![.\n])(?=.*[A-Z])(?=.*[a-z]).*$" required="required" />
                </label>
            </div>
           <div class="row">
             <button type="submit">sign up</button>
           </div>
        </form>
    </div>
</div>
<!--end of signup form popup-->

<!-- BEGIN | Header -->
@include('pages.top-nav')
	    <!-- top search form -->
	  
	</div>
</header>
<!-- END | Header -->

<div class="hero user-hero">
	<div class="container">
		<div class="row">
			<div class="col-md-12">
				<div class="hero-ct">
					{{-- <h1>{{ $user->name }}</h1> --}}
					<ul class="breadcumb">
						<li class="active"><a href="/home">Home</a></li>
						<li> <span class="ion-ios-arrow-right"></span>USER HISTORY</li>
					</ul>
				</div>
			</div>
		</div>
	</div>
</div>
		<div class="buster-light">
<div class="page-single">
	<div class="container">
		<div class="row ipad-width2">
			<div class="col-md-3 col-sm-12 col-xs-12">
				<div class="user-information">
					<div class="user-img">
						<a href="#"><img src="dashboard/images/new/user.png" alt=""><br></a>
						<a href="#" class="redbtn">Change avatar</a>
					</div>
					<div class="user-fav">
						<p>Account Details</p>
						<ul>
							<li><a style="font-size: 13px; font-weight:bold; text-transform:capitalize;">Name: {{$user->name }}</a></li>
							<li ><a style="font-size: 13px; font-weight:bold; text-transform:capitalize">Email: {{$user->email }}</a></li>
							<li ><a style="font-size: 15px; font-weight:bold; text-transform:capitalize">Password: *******</a></li>
						</ul>
					</div>
					<div class="user-fav">
						<p>Others</p>
						<ul>
                            <li class="active"><a href="#">Recent Jobs</a></li>
                            <li ><a href="#">Completed Jobs</a></li>
							<li><a href="#">Change password</a></li>
							<li><a  href="{{ url('logout') }}">Log out</a></li>
						</ul>
					</div>
				</div>
			</div>
			<div class="col-md-9 col-sm-12 col-xs-12">
				<div class="topbar-filter">
					<p>Found <span>2 Job</span> in total</p>
				
				</div>
                <div class="movie-item-style-2 userrate">
					{{-- <img src="dashboard/images/new/sand-clock.png" alt=""> --}}
                   
					<div class="mv-item-infor">
                        <div style="display: flex">
                            <p class="time sm" style="margin-right:5px">19 June 2021</p> <img src="dashboard/images/new/hourglass.png" alt="hourglass" style="width:20px;height:20px">
                        </div>  
                        <p>Helper : Joel Adukwu</p>
						<p>Service : CAC Registration</p>	
                        <p>Cost: 43,000</p>	
                        <div style="display: flex">
                            <p>Duration: 2 Weeks</p> <p style="color:Orange; margin-left:10px"> Remaining: 4 Days</p>
                        </div>
                       <div style="display:flex">	<p class="time sm-text" style="margin-right:10px; font-size:8px; color:white;background-color:#00b300">Completed Job</p> 	<p class="time sm-text" style="font-size:8px; color:white;background-color:red">Report Job</p></div>
                        
						
                    </div>
				</div>
                <div class="movie-item-style-2 userrate">
					{{-- <img src="dashboard/images/new/sand-clock.png" alt=""> --}}
                   
					<div class="mv-item-infor">
                        <div style="display: flex">
                            <p class="time sm" style="margin-right:5px">18 June 2021</p> <img src="dashboard/images/new/hourglass.png" alt="hourglass" style="width:20px;height:20px">
                        </div>  
                        <p>Helper : Samuel Philip</p>
						<p>Service : Land Agreement</p>	
                        <p>Cost: 18,000</p>	
                        <div style="display: flex">
                            <p>Duration: 3 Days</p> <p style="color:red; margin-left:10px;"> Remaining: 0 Days</p>
                        </div>
                       <div style="display:flex">	<p class="time sm-text" style="margin-right:10px; font-size:8px; color:white;background-color:#00b300">Completed Job</p> 	<p class="time sm-text" style="font-size:8px; color:white;background-color:red">Report Job</p></div>
                        
						
                    </div>
				</div>
			
				
			</div>
		</div>
	</div>
</div>
		</div>
<!-- footer section-->
@include('pages.footer')
<!-- end of footer section-->

<script src="{{URL::asset('dashboard/js/jquery.js')}}"></script>
<script src="{{URL::asset('dashboard/js/plugins.js')}}"></script>
<script src="{{URL::asset('dashboard/js/plugins2.js')}}"></script> 
<script src="{{URL::asset('dashboard/js/custom.js')}}"></script>
</body>

<!-- userrate_light16:31-->
</html>