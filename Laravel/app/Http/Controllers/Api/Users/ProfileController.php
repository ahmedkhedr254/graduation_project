<?php

namespace App\Http\Controllers\Api\Users;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\User;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Str;

class ProfileController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        //
        $users = User::all();
        return response(['status' => true, 'users' => $users]);
    }

    /**
     * Store a newly created resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @return \Illuminate\Http\Response
     */
    public function store(Request $request)
    {
        //
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
            $user->is_blind = request('is_blind');
            $user->password = bcrypt(request('password'));
            $user->api_token = Str::random(60);
            $user->save();
            auth()->attempt(['email' => \request('email'), 'password' => \request('password')]);
            $user = auth()->user();
            $user->api_token = Str::random(60);
            $user->save();
            return response(['status' => true, 'user' => $user, 'token' => $user->api_token]);
        }
    }

    /**
     * Display the specified resource.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function show($id)
    {
        //
        $user = User::find($id);
        if(isset($user)) {
            return response(['status' => true, 'user' => $user]);
        }else{
            return response(['status' => false, 'messages' => 'User not found']);
        }
    }

    /**
     * Update the specified resource in storage.
     *
     * @param  \Illuminate\Http\Request  $request
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function update(Request $request, $id)
    {
        //
        $user = User::find($id);
        if(!isset($user)) {
            return response(['status' => false, 'messages' => 'User not found']);
        }

        if (\request('old') == $user->password){
            return response(['status' => false, 'messages' => 'Wrong Password']);
        }

        $validator =  Validator::make(\request()->all(), [
            'first' => ['required', 'string', 'max:255'],
            'last' => ['required', 'string', 'max:255'],
            'is_blind' => ['required', 'boolean'],
            'password' => ['required', 'string', 'min:8'],
        ]);
        if ($validator->fails()){
            return response(['status' => false, 'messages' => $validator->messages()]);
        }else {
            $user->first_name = request('first');
            $user->last_name = request('last');
            $user->is_blind = request('is_blind');
            $user->password = bcrypt(request('password'));
            $user->save();
            return response(['status' => true, 'user' => $user]);
        }
    }

    /**
     * Remove the specified resource from storage.
     *
     * @param  int  $id
     * @return \Illuminate\Http\Response
     */
    public function destroy($id)
    {
        //
        $user = User::find($id);
        if(!isset($user)) {
            return response(['status' => false, 'messages' => 'User not found']);
        }
        $user->delete();
        return response(['status' => true, 'messages' => 'User deleted successfully']);
    }
}
