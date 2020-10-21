<?php

namespace App\Http\Controllers\Users;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class LoginController extends Controller
{
    //
    public function login_get(){
        if(auth()->check()){
            return redirect('home');
        }else{
            return view('auth.login');
        }

    }

    public function login_post(){

        $remember = \request()->has('remember')?true:false;
        if (auth()->attempt(['email'=>\request('email'), 'password'=>\request('password')], $remember)){
            return redirect('home');
        }else{
            return back();
        }

    }

    public function logout(){
        auth()->logout();
        return redirect('login');
    }
}
