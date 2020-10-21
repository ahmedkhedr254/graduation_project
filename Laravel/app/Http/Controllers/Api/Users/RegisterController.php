<?php

namespace App\Http\Controllers\Api\Users;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;
use App\User;
use Illuminate\Support\Str;

class RegisterController extends Controller
{
    //
    public function register(){
        $validator =  Validator::make(\request()->all(), [
            'first' => ['required', 'string', 'max:255'],
            'last' => ['required', 'string', 'max:255'],
            'email' => ['required', 'string', 'email', 'max:255', 'unique:users'],
            'password' => ['required', 'string', 'min:8'],
            'is_blind' => ['required', 'boolean'],
        ]);
        if ($validator->fails()){
            return response(['status' => false, 'messages' => $validator->messages()]);
        }else {
            $user = new User;
            $user->first_name = request('first');
            $user->last_name = request('last');
            $user->email = request('email');
            $user->password = bcrypt(request('password'));
            $user->is_blind = request('is_blind');
            $user->api_token = Str::random(60);
            $user->save();
            auth()->attempt(['email' => \request('email'), 'password' => \request('password')]);
            $user = auth()->user();
            $user->api_token = Str::random(60);
            $user->save();
            return response(['status' => true, 'user' => $user, 'token' => $user->api_token]);
        }
    }
}
