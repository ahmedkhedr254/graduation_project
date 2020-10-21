<?php

namespace App\Http\Controllers\Api\Users;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Str;
use Illuminate\Support\Facades\Validator;

class LoginController extends Controller
{
    //
    public function login(){

        $validator = Validator::make(\request()->all(), [
            'email' => ['required', 'string', 'email', 'max:255'],
            'password' => ['required', 'string', 'min:8'],
        ]);

        if ($validator->fails()){
            return response(['status' => false, 'messages' => $validator->messages()]);
        }else {
            if (auth()->attempt(['email' => \request('email'), 'password' => \request('password')])) {
                $user = auth()->user();
                $user->api_token = Str::random(60);
                $user->save();
                return response(['status' => true, 'user' => $user, 'token' => $user->api_token]);
            } else {
                return response(['status' => false, 'messages' => 'Invalid Email Or Password']);
            }
        }

    }
}
