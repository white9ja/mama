<?php

namespace App\Http\Controllers;

use App\User;
use App\SubAccount;
use App\Subplan;
use App\Domain;
use Illuminate\Http\Request;
use Illuminate\Support\Str;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Hash;
use Illuminate\Support\Facades\Redirect;
use GuzzleHttp\Exception\ClientException;
use Illuminate\Support\Facades\Password;
use Illuminate\Auth\Passwords\DatabaseTokenRepository;
use Illuminate\Support\Facades\Session;
use App\Events\PasswordReset;
use Segment;
use Config;
use Carbon\Carbon;

class AuthController extends Controller
{
    public function showLoginForm()
    {
        if(Auth::check())
        {
            return Session::get('url.intended') != url('/') ? redirect(session('url.intended')) : redirect('dashboard');
        }

        if(!session()->has('url.intended'))
        {
            session(['url.intended' => url()->previous()]);
        }
        
        return view('auth.login');
    }

    public function login(Request $request)
    {
        $email = $request->get('email');
        $remember = $request->get('remember');
        if(Auth::attempt([
            'email' => $request->get('email'),
            'password' => $request->get('password')], $remember))
        {
            $user = User::where('email', $email)->first();

            if(app()->environment('production'))
            {
                $account_owner = $user;
                if($user->role_id == 3)
                {
                    $account_owner = $user->userLeader;
                }
                
                $account_plan = $account_owner->subscribed('main') ? Config::get('constant.plan_name.'.$user->subscription('main')->stripe_plan) : "free";

                Segment::init(Config::get('constant.segment.key'));
                Segment::identify(array(
                    "userId" => $user->id,
                    "traits" => array(
                        "name" => $user->firstname,
                        "email" => $user->email,
                        "date_sign_up" => $user->created_at,
                        "account_plan" => $account_plan,
                        "account_owner" => $account_owner->firstname,
                    )
                ));

                Segment::track(array(
                    "userId" => $user->id,
                    "event" => "Logged in",
                    "properties" => array(
                        "login_date" => Carbon::now(),
                    )
                ));
                Segment::flush();
            }

            return Session::get('url.intended') != url('/') ? redirect(session('url.intended')) : redirect('dashboard');
            // return redirect('dashboard');
        }
        else
        {
            return back()->with('error', "Login Failed");
        }
    }

    public function showRegistrationForm()
    {
        return view('auth.signup');
    }

    public function showRegistrationFormStripeUser()
    {
        if(Auth::check())
        {
            return redirect('dashboard');
        }
        if(app()->environment('production'))
        {
            Segment::init(Config::get('constant.segment.key'));
            Segment::track(array(
                "anonymousId" => Str::uuid(),
                "event" => "Signup Viewed",
                "properties" => array(
                    "date_viewed" => Carbon::now()
                )
            )); 
            Segment::flush();
        }

        return view('auth.signup_stripe_users');
    }

    public function register(Request $request)
    {
        $data = $request->all();
        if($request->validate([
            'firstname' => 'required|string|min:3|max:50',
            'email' => 'required|string|email|max:50|unique:users',
            'password' => 'required|string|min:6',
            'terms' =>'accepted'
        ]))
        {
            $user = new User();
            $user->fill($data);        
            $user->password = bcrypt($user->password);
            $user->api_token = $this->randomString();
            $user->sso_token = Str::uuid();
            $user->save();

            // Create a default sub account for new users
            $subAccount = new SubAccount();
            $subAccount->account_name = "Default";
            $subAccount->user_id = $user->id;
            $subAccount->confirmed = 1;
            $subAccount->save();

            //update current sub account of users
            $user->current_sub_account_id = $subAccount->id;
            $user->save();

            //send User Details to Joyworks and Funneljoy
            if (app()->environment('production'))
            {
                //Send To Joyworks

                $client = new \GuzzleHttp\Client();
                    $url = "https://joyworks.io/a49ada1c-a7e5-11ea-bb37-0242ac130002?name=".$user->name."&email=".$user->email."&password=".$user->password."&token=".$user->sso_token;
                    try {
                        $client->request('POST', $url);
                    } catch (ClientException $e) {
                        Log::info('Was Unable to transfer the following email to Joyworks during register - '.$user->email);
                    }
                
                    //Send User Details to Funneljoy

                    $client = new \GuzzleHttp\Client();
                    $url = "https://funneljoy.com/b2200950-c2cd-494e-9ccd-b91960c92663?name=".$user->name."&email=".$user->email."&password=".$user->password."&token=".$user->sso_token;
                    try {
                        $client->request('POST', $url);
                    } catch (ClientException $e) {
                        Log::info('Was Unable to transfer the following email to Funneljoy during register - '.$user->email);
                    }
            }

            Subplan::create(['user_id'=>$user->id, 'fe'=>2, 'oto1'=>1]);

            // return view('profile')->with('user', $data);
            Auth::loginUsingId($user->id);
            return redirect('dashboard');
        }
    }

    public function registerStripeUser(Request $request)
    {
        $data = $request->all();
        if($request->validate([
            'firstname' => 'required|string|min:3|max:50',
            'email' => 'required|string|email|max:50|unique:users',
            'password' => 'required|string|min:6',
            'terms' =>'accepted'
        ]))
        {
            $user = new User();
            $user->fill($data);        
            $user->password = bcrypt($user->password);
            $user->api_token = $this->randomString();
            $user->sso_token = Str::uuid();
            $user->is_stripe_user = 1;
            $user->save();


            //send User Details to Joyworks and Funneljoy
            if (app()->environment('production'))
            {
                //Send To Joyworks

                $client = new \GuzzleHttp\Client();
                    $url = "https://joyworks.io/a49ada1c-a7e5-11ea-bb37-0242ac130002?name=".$user->firstname."&email=".$user->email."&password=".$user->password."&token=".$user->sso_token;
                    try {
                        $response =  $client->request('POST', $url);
                    } catch (ClientException $e) {
                        Log::info($e->getResponse());
                        Log::info('Was Unable to transfer the following email to Joyworks during register - '.$user->email);
                    }
                
                    //Send User Details to Funneljoy

                    $client = new \GuzzleHttp\Client();
                    $url = "https://funneljoy.com/b2200950-c2cd-494e-9ccd-b91960c92663?name=".$user->firstname."&email=".$user->email."&password=".$user->password."&token=".$user->sso_token;
                    try {
                        $response = $client->request('POST', $url);
                    } catch (ClientException $e) {
                        Log::info($e->getResponse());
                        Log::info('Was Unable to transfer the following email to Funneljoy during register - '.$user->email);
                    }
            }

            // Create a default sub account for new users
            $subAccount = new SubAccount();
            $subAccount->account_name = "Default";
            $subAccount->user_id = $user->id;
            $subAccount->confirmed = 1;
            $subAccount->save();

            //update current sub account of users
            $user->current_sub_account_id = $subAccount->id;
            $user->save();

            Subplan::create(['user_id'=>$user->id, 'fe'=>2, 'oto1'=>1]);

            // return view('profile')->with('user', $data);
            Auth::loginUsingId($user->id);
            return redirect('dashboard');
        }
    }



    /**
     * Log the user out of the application.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function logout(Request $request){

        // if (app()->environment('production')){
        //     if(is_null($request->src)){
        //         return redirect()->away('https://funneljoy.com/logout?src=pj&rdr=pj'); //fj
        //     }
    
        //     if($request->src == "fj"){
        //         if($request->rdr == "fj"){
        //             Auth::guard()->logout();
        //             $request->session()->invalidate();
        //             return redirect()->away('https://funneljoy.com/logout?src=pj&rdr=fj'); //fj
        //         }elseif($request->rdr == "pj"){
        //             return redirect()->away('https://joyworks.io/logout?src=pj&rdr=pj'); //jw
        //         }
        //     }
    
        //     if($request->src == "jw"){
        //         if($request->rdr == "jw"){
        //             Auth::guard()->logout();
        //             $request->session()->invalidate();
        //             return redirect()->away('https://joyworks.io/logout?src=pj&rdr=jw'); //jw
        //         }elseif($request->rdr == "pj"){
        //             Auth::guard()->logout();
        //             $request->session()->invalidate();
        //             return redirect('/');
        //         }
        //     }
        // }

        Auth::guard()->logout();
        $request->session()->invalidate();
        return redirect('/');

    }
    
    
    
    
    /**
	 * Display the password reminder view.
	 *
	 * @return Response
	 */
    public function getRemind()
    {
        return view('auth/passwords/email');
    }

    /**
	 * Handle a POST request to remind a user of their password.
	 *
	 * @return Response
	 */
    public function postRemind(Request $request)
    {
        $data = $request->all();
        $hasher = \App::make('hash');
        $reminders = new DatabaseTokenRepository(\DB::connection(), $hasher, \Config::get('auth.passwords.users.table'), \Config::get('app.key'));
        $user = \Password::getUser(['email' => $data['email']]);
        if($user != null)
        {
            $token = $reminders->create($user);
            $data = $user->toArray();
            $data['name'] = $user->firstname;
            $data['token'] = $token;

            \Mail::send('emails.reminder', $data, function($mail) use($data){
                $mail->to($data['email'], $data['firstname'].' '.$data['lastname']);
                $mail->from('support@pixeljoyapp.com');
                $mail->subject('Your PixelPro Password');
            });
        }
        return back()->with('status', \Lang::get("If this email exists, we have sent a password reset. Check your email to continue"));
    }

    /**
	 * Display the password reset view for the given token.
	 *
	 * @param  string  $token
	 * @return Response
	 */
    public function getReset($token = null)
    {
        if (is_null($token)) App::abort(404);

        return view('/auth/passwords/reset')->with('token', $token);
    }

    /**
	 * Handle a POST request to reset a user's password.
	 *
	 * @return Response
	 */
    public function postReset(Request $request)
    {
        $data = $request->all();
        // $credentials = Input::only(
        //     'email', 'password', 'password_confirmation', 'token'
        // );
        $credentials = [
            'email' => $data['email'],
            'password' => $data['password'],
            'password_confirmation' => $data['password_confirmation'],
            'token' => $data['token']
        ];
        $newPassword = '';
        $response = Password::reset($credentials, function($user, $password)
        {
            $user->password = Hash::make($password);
            $newPassword = $user->password;
            $user->save();

        });

        switch ($response)
        {
            // case Password::INVALID_PASSWORD: this class does not exist 
            case Password::INVALID_TOKEN:
            case Password::INVALID_USER:
                return back()->with('error', \Lang::get($response));

            case Password::PASSWORD_RESET:
                // I need to access the User Email and Password in this case
                event(new PasswordReset(User::where('email', $data['email'])->first()));

                return redirect('login')->with('success', 'Password Changed Successfully, Proceed to Login');
        }
    }

    public function randomString()
    {
        do
        {
            $random = str_random(60);
            $user = User::where('api_token', $random)->first();
        }
        while(!empty($user));

        return $random;
    }

    public function comingSoon()
    {
        if(\Request::gethost() != "localhost" && \Request::gethost() != "pixeljoy.com" && \Request::gethost() != "www.pixeljoy.com" && \Request::gethost() != "127.0.0.1")
        {
            $domain = Domain::where('domain_name', \Request::gethost())->first();
            if($domain)
            {
                $user = $domain->subaccount->user;
                if($user->role_id == 3)
                {
                    $user = $user->userLeader;
                }
                
                if(!$user->restrictUser("subscribed"))
                {
                    if($domain->main_redirect_url)
                    {
                        return Redirect::to($domain->main_redirect_url);
                    }
                }
            }
            else
            {
                return view('errors.default');
            }
        }

        return Redirect::to('https://pixlypro.kyvio.com/earlybird-v2');
    }
}
