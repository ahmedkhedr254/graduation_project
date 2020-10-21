<?php

namespace App\Http\Controllers\Users;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\Validator;
use App\User;
use Illuminate\Support\Str;

class RegisterController extends Controller
{
    //
    public function register_get(){
        if(auth()->check()){
            return redirect('home');
        }else{
            return view('auth.register');
        }
    }

    public function register_post(){

        \request()->validate([
            'first' => ['required', 'string', 'max:255'],
            'last' => ['required', 'string', 'max:255'],
            'email' => ['required', 'string', 'email', 'max:255', 'unique:users'],
            'password' => ['required', 'string', 'min:8', 'confirmed'],
        ]);
        $user = new User;
        $user->first_name = request('first');
        $user->last_name = request('last');
        $user->email = request('email');
        $user->password = bcrypt(request('password'));
        $user->api_token = Str::random(60);
        $user->save();
        auth()->attempt(['email'=>\request('email'), 'password'=>\request('password')], true);
        return redirect('home');

    }
}
