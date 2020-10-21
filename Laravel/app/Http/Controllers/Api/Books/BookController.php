<?php

namespace App\Http\Controllers\Api\Books;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Book;
use Illuminate\Support\Facades\Validator;
use Illuminate\Validation\Rule;

class BookController extends Controller
{
    /**
     * Display a listing of the resource.
     *
     * @return \Illuminate\Http\Response
     */
    public function index()
    {
        //
        $books = Book::all();
        return response(['status' => true, 'books' => $books]);
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
            'name' => ['required', 'string', 'max:255'],
            'author' => ['required', 'string', 'max:255'],
            'status' => [
                'required',
                Rule::in(['private', 'public']),
            ],
            'description' => ['required', 'string', 'max:1023'],
            'publishing_house' => ['required', 'string', 'max:255'],
            'publishing_date' => ['required', 'date', 'max:255'],
            'no_pages' => ['required', 'integer'],
        ]);
        if ($validator->fails()){
            return response(['status' => false, 'messages' => $validator->messages()]);
        }else {
            $book = new Book;
            $book->name = request('name');
            $book->author = request('author');
            $book->status = request('status');
            $book->description = request('description');
            $book->publishing_house = request('publishing_house');
            $book->publishing_date = request('publishing_date');
            $book->no_pages = request('no_pages');
            $book->user_id = \request()->user()->id;
            $book->save();
            return response(['status' => true, 'book' => $book]);
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
        $book = Book::find($id);
        if(isset($book)) {
            return response(['status' => true, 'book' => $book]);
        }else {
            return response(['status' => false, 'messages' => 'Book not found']);
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
        $book = Book::find($id);
        if(isset($book)) {
            $validator =  Validator::make(\request()->all(), [
                'name' => ['required', 'string', 'max:255'],
                'author' => ['required', 'string', 'max:255'],
                'status' => [
                    'required',
                    Rule::in(['private', 'public']),
                ],
                'description' => ['required', 'string', 'max:1023'],
                'publishing_house' => ['required', 'string', 'max:255'],
                'publishing_date' => ['required', 'date', 'max:255'],
                'no_pages' => ['required', 'integer'],
            ]);
            if ($validator->fails()){
                return response(['status' => false, 'messages' => $validator->messages()]);
            }else {
                $book->name = request('name');
                $book->author = request('author');
                $book->status = request('status');
                $book->description = request('description');
                $book->publishing_house = request('publishing_house');
                $book->publishing_date = request('publishing_date');
                $book->no_pages = request('no_pages');
                $book->save();
                return response(['status' => true, 'book' => $book]);
            }
        }else {
            return response(['status' => false, 'messages' => 'Book not found']);
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
        $book = Book::find($id);
        if(isset($book)) {
            $book->delete();
            return response(['status' => true, 'messages' => 'Book deleted successfully']);
        }else {
            return response(['status' => false, 'messages' => 'Book not found']);
        }
    }
}
